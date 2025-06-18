from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from models import Project, ProjectCategory
from database import db
from sqlalchemy import or_
from . import git_bp

@git_bp.route('/')
def index():
    print(f"DEBUG: Accessing git blueprint index route. Attempting to render 'git/index.html'")
    
    # Get filter parameters
    category_id = request.args.get('category', type=int)
    project_type = request.args.get('type')  # 'opensource' or 'commercial'
    status = request.args.get('status')
    search_query = request.args.get('q', '')
    
    # Update GitHub data in background for projects that need it (async approach)
    # Only update a few projects per request to avoid blocking
    projects_to_update = Project.query.filter(
        Project.github_url.isnot(None)
    ).limit(5).all()  # Get up to 5 projects that have GitHub URLs
    
    # Filter projects that actually need updates
    projects_needing_update = [p for p in projects_to_update if p.should_update_github_data()]
    
    updated_any = False
    for project in projects_needing_update[:3]:  # Limit to 3 updates per request
        if project.fetch_github_data():
            updated_any = True
    
    if updated_any:
        try:
            db.session.commit()
        except Exception as e:
            print(f"Error committing GitHub data updates: {e}")
            db.session.rollback()
    
    # Base query
    query = Project.query
    
    # Apply filters
    if category_id:
        query = query.filter(Project.category_id == category_id)
    
    if project_type == 'opensource':
        query = query.filter(Project.is_opensource == True)
    elif project_type == 'commercial':
        query = query.filter(Project.is_opensource == False)
    
    if status:
        query = query.filter(Project.status == status)
    
    if search_query:
        query = query.filter(or_(
            Project.title.ilike(f'%{search_query}%'),
            Project.description.ilike(f'%{search_query}%'),
            Project.technologies.ilike(f'%{search_query}%')
        ))
    
    # Order by featured first, then by creation date
    projects = query.order_by(Project.is_featured.desc(), Project.created_at.desc()).all()
    categories = ProjectCategory.query.all()
    
    template_name_to_render = 'git/index.html'
    jinja_env = current_app.jinja_env
    try:
        template_object = jinja_env.get_template(template_name_to_render)
        print(f"DEBUG: Jinja2 resolved '{template_name_to_render}' to file: {template_object.filename}")
    except Exception as e:
        print(f"DEBUG: Error getting template '{template_name_to_render}' from Jinja2 env: {e}")
    
    return render_template(template_name_to_render, 
                         projects=projects, 
                         categories=categories,
                         current_category=category_id,
                         current_type=project_type,
                         current_status=status,
                         search_query=search_query)

@git_bp.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        projects = Project.query.filter(or_(
            Project.title.ilike(f'%{query}%'),
            Project.description.ilike(f'%{query}%'),
            Project.technologies.ilike(f'%{query}%')
        )).all()
    else:
        projects = []
    # Also update search.html if it's in git/templates
    return render_template('git/search.html', projects=projects, query=query) # Assuming search.html is in git/templates

@git_bp.route('/api/projects')
def api_projects():
    """API endpoint for dynamic project filtering"""
    category_id = request.args.get('category', type=int)
    project_type = request.args.get('type')
    status = request.args.get('status')
    search_query = request.args.get('q', '')
    
    query = Project.query
    
    if category_id:
        query = query.filter(Project.category_id == category_id)
    
    if project_type == 'opensource':
        query = query.filter(Project.is_opensource == True)
    elif project_type == 'commercial':
        query = query.filter(Project.is_opensource == False)
    
    if status:
        query = query.filter(Project.status == status)
    
    if search_query:
        query = query.filter(or_(
            Project.title.ilike(f'%{search_query}%'),
            Project.description.ilike(f'%{search_query}%'),
            Project.technologies.ilike(f'%{search_query}%')
        ))
    
    projects = query.order_by(Project.is_featured.desc(), Project.created_at.desc()).all()
    
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'image_url': p.image_url,
        'github_url': p.github_url,
        'live_url': p.live_url,
        'technologies': p.technologies.split(',') if p.technologies else [],
        'category': p.category.name if p.category else None,
        'is_featured': p.is_featured,
        'is_opensource': p.is_opensource,
        'stars': p.stars,
        'forks': p.forks,
        'status': p.status,
        'created_at': p.created_at.isoformat() if p.created_at else None,
        'last_updated': p.last_updated.isoformat() if p.last_updated else None
    } for p in projects])

@git_bp.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('git/project.html', project=project)

@git_bp.route('/api/github/cache-stats')
def github_cache_stats():
    """Get GitHub cache statistics"""
    try:
        from github_service import github_service
        stats = github_service.get_cache_stats()
        
        # Add rate limit info if available
        rate_limit = github_service.get_rate_limit_info()
        if rate_limit:
            stats['rate_limit'] = rate_limit
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@git_bp.route('/api/github/clear-cache', methods=['POST'])
def clear_github_cache():
    """Clear GitHub cache (admin only)"""
    try:
        from github_service import github_service
        repo_name = request.json.get('repo') if request.is_json else None
        
        if repo_name:
            # Clear cache for specific repo
            if '/' in repo_name:
                username, repo = repo_name.split('/', 1)
                github_service.clear_cache_for_repo(username, repo)
                message = f'Cleared cache for {repo_name}'
            else:
                return jsonify({'error': 'Invalid repository format. Use username/repo'}), 400
        else:
            # Clear all cache
            github_service.clear_all_cache()
            message = 'Cleared all GitHub cache'
        
        return jsonify({'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@git_bp.route('/api/github/force-refresh/<int:project_id>', methods=['POST'])
def force_refresh_project(project_id):
    """Force refresh GitHub data for a specific project"""
    project = Project.query.get_or_404(project_id)
    
    if not project.github_url:
        return jsonify({'error': 'Project has no GitHub URL'}), 400
    
    username, repo = project.extract_github_repo()
    if not username or not repo:
        return jsonify({'error': 'Invalid GitHub URL'}), 400
    
    try:
        from github_service import github_service
        
        # Force refresh from API
        github_data = github_service.get_repository_data(username, repo, force_refresh=True)
        
        if github_data:
            # Update project with fresh data
            success = project.fetch_github_data()
            if success:
                db.session.commit()
                return jsonify({
                    'message': f'Successfully refreshed data for {username}/{repo}',
                    'data': {
                        'stars': project.stars,
                        'forks': project.forks,
                        'last_updated': project.last_updated.isoformat() if project.last_updated else None
                    }
                })
            else:
                return jsonify({'error': 'Failed to update project data'}), 500
        else:
            return jsonify({'error': 'Failed to fetch GitHub data'}), 404
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500