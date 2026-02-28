"""Enhanced SEO settings with comprehensive meta tags support

Revision ID: seo_enhancement_001
Revises: previous_migration
Create Date: 2024-12-23 10:00:00.000000

"""
from alembic import op

# revision identifiers
revision = 'seo_enhancement_001'
down_revision = None  # Replace with your latest migration
branch_labels = None
depends_on = None

def upgrade():
    # Use IF NOT EXISTS to safely add columns that may already exist.
    # op.add_column aborts the whole PostgreSQL transaction on duplicates,
    # so we use raw DDL instead.
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS twitter_title VARCHAR(200)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS twitter_description TEXT")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS twitter_image VARCHAR(255)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS twitter_url VARCHAR(255)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS twitter_card VARCHAR(50) DEFAULT 'summary_large_image'")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS og_url VARCHAR(255)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS og_type VARCHAR(50) DEFAULT 'website'")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS hreflang VARCHAR(10) DEFAULT 'en'")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS focus_keywords TEXT")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS meta_author VARCHAR(100)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS meta_publisher VARCHAR(100)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS article_section VARCHAR(100)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS article_tags TEXT")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS page_priority FLOAT DEFAULT 0.5")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS update_frequency VARCHAR(20) DEFAULT 'weekly'")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS noindex BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS nofollow BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS noarchive BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS nosnippet BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS google_analytics_id VARCHAR(50)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS google_tag_manager_id VARCHAR(50)")
    op.execute("ALTER TABLE seo_settings ADD COLUMN IF NOT EXISTS facebook_pixel_id VARCHAR(50)")
    # contact_submission columns (may be missing on older deployments)
    op.execute("ALTER TABLE contact_submission ADD COLUMN IF NOT EXISTS user_agent VARCHAR(500)")
    op.execute("ALTER TABLE contact_submission ADD COLUMN IF NOT EXISTS is_spam BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE contact_submission ADD COLUMN IF NOT EXISTS is_replied BOOLEAN DEFAULT false")
    op.execute("ALTER TABLE contact_submission ADD COLUMN IF NOT EXISTS replied_at TIMESTAMP")

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
