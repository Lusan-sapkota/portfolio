import click
from flask.cli import with_appcontext
from database import db
from models import User, Project

def register_commands(app):
    @app.cli.command('create-admin')
    @click.argument('username')
    @click.argument('email')
    @click.argument('password')
    def create_admin(username, email, password):
        """Create an admin user."""
        user = User.query.filter_by(username=username).first()
        if user:
            click.echo(f'User {username} already exists.')
            return

        user = User(username=username, email=email, is_admin=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        click.echo(f'Admin user {username} created successfully.')

    @app.cli.command('update-github-data')
    @click.option('--force', is_flag=True, help='Force update all projects regardless of last update time')
    @click.option('--project-id', type=int, help='Update specific project by ID')
    @with_appcontext
    def update_github_data_command(force, project_id):
        """Update GitHub data for projects."""
        try:
            from github_service import github_service
            
            if project_id:
                # Update specific project
                project = Project.query.get(project_id)
                if not project:
                    click.echo(f'Project with ID {project_id} not found.')
                    return
                
                if not project.github_url:
                    click.echo(f'Project "{project.title}" has no GitHub URL.')
                    return
                
                username, repo = project.extract_github_repo()
                if username and repo:
                    click.echo(f'Updating GitHub data for {username}/{repo}...')
                    if force:
                        github_service.clear_cache_for_repo(username, repo)
                    
                    if project.fetch_github_data():
                        db.session.commit()
                        click.echo(f'✓ Updated: {project.title} (stars: {project.stars}, forks: {project.forks})')
                    else:
                        click.echo(f'✗ Failed to update: {project.title}')
                else:
                    click.echo(f'Invalid GitHub URL for project "{project.title}": {project.github_url}')
                return
            
            # Update all projects
            projects = Project.query.filter(Project.github_url.isnot(None)).all()
            
            if not projects:
                click.echo('No projects with GitHub URLs found.')
                return
            
            click.echo(f'Found {len(projects)} projects with GitHub URLs.')
            
            if force:
                click.echo('Force mode: clearing all GitHub cache...')
                github_service.clear_all_cache()
            
            updated_count = 0
            failed_count = 0
            skipped_count = 0
            
            for project in projects:
                username, repo = project.extract_github_repo()
                if not username or not repo:
                    click.echo(f'✗ Invalid GitHub URL: {project.title} - {project.github_url}')
                    failed_count += 1
                    continue
                
                # Check if update is needed (unless forced)
                if not force and not project.should_update_github_data():
                    click.echo(f'⏭ Skipped (recently updated): {project.title}')
                    skipped_count += 1
                    continue
                
                click.echo(f'Updating: {username}/{repo} ({project.title})...')
                
                if project.fetch_github_data():
                    updated_count += 1
                    click.echo(f'✓ Updated: {project.title} (stars: {project.stars}, forks: {project.forks})')
                else:
                    failed_count += 1
                    click.echo(f'✗ Failed: {project.title}')
            
            if updated_count > 0:
                db.session.commit()
                click.echo(f'\n🎉 Committed {updated_count} updates to database.')
            
            # Summary
            click.echo(f'\n📊 Summary:')
            click.echo(f'  Updated: {updated_count}')
            click.echo(f'  Failed: {failed_count}')
            click.echo(f'  Skipped: {skipped_count}')
            click.echo(f'  Total: {len(projects)}')
            
            # Cache stats
            stats = github_service.get_cache_stats()
            if stats.get('cache_enabled'):
                click.echo(f'  Cache: {stats.get("cache_type", "Unknown")}')
            
        except Exception as e:
            click.echo(f'Error updating GitHub data: {e}')
            db.session.rollback()

    @app.cli.command('github-cache-stats')
    @with_appcontext 
    def github_cache_stats_command():
        """Show GitHub cache statistics."""
        try:
            from github_service import github_service
            
            stats = github_service.get_cache_stats()
            click.echo('📈 GitHub Cache Statistics:')
            click.echo(f'  Cache Enabled: {stats.get("cache_enabled", False)}')
            click.echo(f'  Cache Type: {stats.get("cache_type", "N/A")}')
            
            # Get rate limit info
            rate_limit = github_service.get_rate_limit_info()
            if rate_limit and 'resources' in rate_limit:
                core = rate_limit['resources'].get('core', {})
                click.echo(f'\n🔄 GitHub API Rate Limit:')
                click.echo(f'  Remaining: {core.get("remaining", "N/A")}/{core.get("limit", "N/A")}')
                
                if core.get('reset'):
                    import datetime
                    reset_time = datetime.datetime.fromtimestamp(core['reset'])
                    click.echo(f'  Resets at: {reset_time.strftime("%Y-%m-%d %H:%M:%S")}')
            
        except Exception as e:
            click.echo(f'Error getting cache stats: {e}')

    @app.cli.command('clear-github-cache')
    @click.option('--repo', help='Clear cache for specific repo (username/repo)')
    @with_appcontext
    def clear_github_cache_command(repo):
        """Clear GitHub cache."""
        try:
            from github_service import github_service
            
            if repo:
                if '/' not in repo:
                    click.echo('Error: Repository must be in format username/repo')
                    return
                
                username, repo_name = repo.split('/', 1)
                github_service.clear_cache_for_repo(username, repo_name)
                click.echo(f'✅ Cleared cache for {repo}')
            else:
                github_service.clear_all_cache()
                click.echo('✅ Cleared all GitHub cache')
                
        except Exception as e:
            click.echo(f'Error clearing cache: {e}')