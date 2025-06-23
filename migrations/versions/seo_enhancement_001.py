"""Enhanced SEO settings with comprehensive meta tags support

Revision ID: seo_enhancement_001
Revises: previous_migration
Create Date: 2024-12-23 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'seo_enhancement_001'
down_revision = None  # Replace with your latest migration
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to seo_settings table
    try:
        # Twitter fields
        op.add_column('seo_settings', sa.Column('twitter_title', sa.String(200), nullable=True))
        op.add_column('seo_settings', sa.Column('twitter_description', sa.Text(), nullable=True))
        op.add_column('seo_settings', sa.Column('twitter_image', sa.String(255), nullable=True))
        op.add_column('seo_settings', sa.Column('twitter_url', sa.String(255), nullable=True))
        op.add_column('seo_settings', sa.Column('twitter_card', sa.String(50), nullable=True, server_default='summary_large_image'))
        
        # Enhanced Open Graph fields
        op.add_column('seo_settings', sa.Column('og_url', sa.String(255), nullable=True))
        op.add_column('seo_settings', sa.Column('og_type', sa.String(50), nullable=True, server_default='website'))
        
        # Additional SEO fields
        op.add_column('seo_settings', sa.Column('hreflang', sa.String(10), nullable=True, server_default='en'))
        op.add_column('seo_settings', sa.Column('focus_keywords', sa.Text(), nullable=True))
        op.add_column('seo_settings', sa.Column('meta_author', sa.String(100), nullable=True))
        op.add_column('seo_settings', sa.Column('meta_publisher', sa.String(100), nullable=True))
        op.add_column('seo_settings', sa.Column('article_section', sa.String(100), nullable=True))
        op.add_column('seo_settings', sa.Column('article_tags', sa.Text(), nullable=True))
        
        # Technical SEO
        op.add_column('seo_settings', sa.Column('page_priority', sa.Float(), nullable=True, server_default='0.5'))
        op.add_column('seo_settings', sa.Column('update_frequency', sa.String(20), nullable=True, server_default='weekly'))
        op.add_column('seo_settings', sa.Column('noindex', sa.Boolean(), nullable=True, server_default='false'))
        op.add_column('seo_settings', sa.Column('nofollow', sa.Boolean(), nullable=True, server_default='false'))
        op.add_column('seo_settings', sa.Column('noarchive', sa.Boolean(), nullable=True, server_default='false'))
        op.add_column('seo_settings', sa.Column('nosnippet', sa.Boolean(), nullable=True, server_default='false'))
        
        # Analytics
        op.add_column('seo_settings', sa.Column('google_analytics_id', sa.String(50), nullable=True))
        op.add_column('seo_settings', sa.Column('google_tag_manager_id', sa.String(50), nullable=True))
        op.add_column('seo_settings', sa.Column('facebook_pixel_id', sa.String(50), nullable=True))
        
    except Exception as e:
        print(f"Migration warning: {e}")
        # Some columns might already exist, continue anyway
        pass

def downgrade():
    # Remove the added columns
    try:
        op.drop_column('seo_settings', 'facebook_pixel_id')
        op.drop_column('seo_settings', 'google_tag_manager_id')
        op.drop_column('seo_settings', 'google_analytics_id')
        op.drop_column('seo_settings', 'nosnippet')
        op.drop_column('seo_settings', 'noarchive')
        op.drop_column('seo_settings', 'nofollow')
        op.drop_column('seo_settings', 'noindex')
        op.drop_column('seo_settings', 'update_frequency')
        op.drop_column('seo_settings', 'page_priority')
        op.drop_column('seo_settings', 'article_tags')
        op.drop_column('seo_settings', 'article_section')
        op.drop_column('seo_settings', 'meta_publisher')
        op.drop_column('seo_settings', 'meta_author')
        op.drop_column('seo_settings', 'focus_keywords')
        op.drop_column('seo_settings', 'hreflang')
        op.drop_column('seo_settings', 'og_type')
        op.drop_column('seo_settings', 'og_url')
        op.drop_column('seo_settings', 'twitter_card')
        op.drop_column('seo_settings', 'twitter_url')
        op.drop_column('seo_settings', 'twitter_image')
        op.drop_column('seo_settings', 'twitter_description')
        op.drop_column('seo_settings', 'twitter_title')
    except Exception as e:
        print(f"Downgrade warning: {e}")
        pass
