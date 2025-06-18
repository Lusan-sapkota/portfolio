"""merge wiki and project category migrations

Revision ID: 37eaa6fd1de6
Revises: c39b9ef784f6, ea8ced3f52e3, project_categories_v1
Create Date: 2025-06-17 21:34:48.293539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37eaa6fd1de6'
down_revision = ('c39b9ef784f6', 'ea8ced3f52e3', 'project_categories_v1')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
