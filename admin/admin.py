from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db
from models import User, Project, WikiArticle, Settings

# Create a secure ModelView that checks authentication
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

# Initialize Flask-Admin
admin = Admin(app, name="Portfolio Admin", template_mode='bootstrap4')

# Add model views
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Project, db.session))
admin.add_view(SecureModelView(WikiArticle, db.session))
admin.add_view(SecureModelView(Settings, db.session))