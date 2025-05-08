import click
from flask.cli import with_appcontext
from database import db
from models import User

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