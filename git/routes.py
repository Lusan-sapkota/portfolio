from flask import Blueprint, render_template, request, redirect, url_for, current_app # Added current_app
from models import Project
from sqlalchemy import or_
from . import git_bp

@git_bp.route('/')
def index():
    print(f"DEBUG: Accessing git blueprint index route. Attempting to render 'git/index.html'") # Updated log
    projects = Project.query.order_by(Project.created_at.desc()).all()
    
    template_name_to_render = 'git/index.html' # Changed
    jinja_env = current_app.jinja_env
    try:
        template_object = jinja_env.get_template(template_name_to_render)
        print(f"DEBUG: Jinja2 resolved '{template_name_to_render}' to file: {template_object.filename}")
    except Exception as e:
        print(f"DEBUG: Error getting template '{template_name_to_render}' from Jinja2 env: {e}")
    
    return render_template(template_name_to_render, projects=projects) # Changed

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

@git_bp.route('/project/<int:project_id>')
def project(project_id):
    project = Project.query.get_or_404(project_id)
    # Also update project.html if it's in git/templates
    return render_template('git/project.html', project=project) # Assuming project.html is in git/templates