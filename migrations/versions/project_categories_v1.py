"""Add project categories and enhanced project fields

Revision ID: project_categories_v1
Revises: a2574e4d0105
Create Date: 2025-06-17 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'project_categories_v1'
down_revision = 'a2574e4d0105'
branch_labels = None
depends_on = None


def upgrade():
    # Create project_category table
    op.create_table('project_category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Add new columns to project table
    op.add_column('project', sa.Column('category_id', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('is_featured', sa.Boolean(), nullable=True))
    op.add_column('project', sa.Column('is_opensource', sa.Boolean(), nullable=True))
    op.add_column('project', sa.Column('stars', sa.Integer(), nullable=True))
    op.add_column('project', sa.Column('status', sa.String(length=20), nullable=True))
    
    # Create foreign key constraint
    op.create_foreign_key(None, 'project', 'project_category', ['category_id'], ['id'])
    
    # Set default values for existing projects
    op.execute("UPDATE project SET is_featured = FALSE WHERE is_featured IS NULL")
    op.execute("UPDATE project SET is_opensource = TRUE WHERE is_opensource IS NULL")
    op.execute("UPDATE project SET stars = 0 WHERE stars IS NULL")
    op.execute("UPDATE project SET status = 'completed' WHERE status IS NULL")
    
    # Insert default categories
    op.execute("""
        INSERT INTO project_category (name, description, icon, color) VALUES
        ('Web Development', 'Full-stack web applications and websites', 'fas fa-globe-americas', '#f39c12'),
        ('Mobile Apps', 'iOS and Android mobile applications', 'fas fa-mobile-alt', '#e74c3c'),
        ('Data Science', 'Machine learning and data analysis projects', 'fas fa-chart-line', '#3498db'),
        ('DevOps', 'Infrastructure and deployment automation', 'fas fa-server', '#2ecc71'),
        ('Open Source', 'Community-driven open source projects', 'fab fa-osi', '#9b59b6'),
        ('Commercial', 'Client work and commercial solutions', 'fas fa-briefcase', '#34495e'),
        ('API Development', 'RESTful APIs and microservices', 'fas fa-plug', '#f1c40f'),
        ('Desktop Apps', 'Cross-platform desktop applications', 'fas fa-desktop', '#95a5a6')
    """)


def downgrade():
    # Remove foreign key constraint
    op.drop_constraint(None, 'project', type_='foreignkey')
    
    # Remove columns from project table
    op.drop_column('project', 'status')
    op.drop_column('project', 'stars')
    op.drop_column('project', 'is_opensource')
    op.drop_column('project', 'is_featured')
    op.drop_column('project', 'category_id')
    
    # Drop project_category table
    op.drop_table('project_category')
