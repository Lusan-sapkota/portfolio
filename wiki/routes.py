from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models import WikiArticle, WikiCategory, SeoSettings
from database import db
from sqlalchemy import or_
from . import wiki_bp
from datetime import datetime
import random

# Helper function to get all top-level categories
def get_categories():
    return WikiCategory.query.filter_by(parent_id=None).all()

# Helper function to get SEO settings
def get_wiki_seo_settings(page_name='wiki'):
    """Get SEO settings for wiki pages"""
    seo = SeoSettings.query.filter_by(page_name=page_name).first()
    return seo

@wiki_bp.route('/')
def index():
    print(f"DEBUG: Accessing wiki blueprint index route.")
    articles = WikiArticle.query.order_by(WikiArticle.title).all()
    categories = get_categories()
    seo = get_wiki_seo_settings('wiki')
    
    return render_template('wiki/index.html', 
                          articles=articles, 
                          categories=categories,
                          active_category=None,
                          active_subcategory=None,
                          current_year=datetime.now().year,
                          seo=seo,
                          page_title=seo.title if seo else "Lusan's Wiki | Technical Knowledge Base",
                          page_description=seo.meta_description if seo else "Comprehensive technical documentation and programming tutorials")

@wiki_bp.route('/search')
def search():
    query = request.args.get('q', '')
    sort_by = request.args.get('sort', 'relevance')  # Default to relevance
    articles_list = []
    categories = get_categories()

    if query:
        # Base query for searching
        base_query = WikiArticle.query.filter(
            or_(
                WikiArticle.title.ilike(f'%{query}%'),
                WikiArticle.content.ilike(f'%{query}%'),
                WikiArticle.summary.ilike(f'%{query}%'),
                WikiArticle.tags.ilike(f'%{query}%')
            )
        )
        
        # Apply sorting
        if sort_by == 'date':
            articles_query = base_query.order_by(WikiArticle.created_at.desc()).all()
        elif sort_by == 'title':
            articles_query = base_query.order_by(WikiArticle.title.asc()).all()
        elif sort_by == 'views':
            articles_query = base_query.order_by(WikiArticle.views.desc()).all()
        else:  # relevance (default)
            # Simple relevance scoring based on where the match occurs
            articles_query = base_query.all()
            
            # Score articles based on where the query appears
            scored_articles = []
            for article in articles_query:
                score = 0
                query_lower = query.lower()
                
                # Title matches get highest score
                if query_lower in article.title.lower():
                    score += 10
                    # Exact title match gets even higher score
                    if query_lower == article.title.lower():
                        score += 20
                
                # Summary matches get medium score
                if article.summary and query_lower in article.summary.lower():
                    score += 5
                
                # Tag matches get medium-high score
                if article.tags and query_lower in article.tags.lower():
                    score += 7
                
                # Content matches get lower score
                if article.content and query_lower in article.content.lower():
                    score += 2
                
                # View count boost (popular articles)
                if article.views:
                    score += min(article.views / 100, 5)  # Max 5 point boost
                
                scored_articles.append((article, score))
            
            # Sort by score (relevance) in descending order
            scored_articles.sort(key=lambda x: x[1], reverse=True)
            articles_query = [article for article, score in scored_articles]
        
        # Convert to dictionaries for template use
        articles_list = []
        for article in articles_query:
            article_dict = article.to_dict()
            # Ensure proper date handling
            if article.created_at:
                article_dict['created_at_formatted'] = article.created_at.strftime('%B %d, %Y')
            else:
                article_dict['created_at_formatted'] = 'Unknown date'
            
            # Add category info
            if article.category:
                article_dict['category'] = {
                    'id': article.category.id,
                    'name': article.category.name
                }
            
            articles_list.append(article_dict)

    if request.accept_mimetypes.accept_json and \
       not request.accept_mimetypes.accept_html:
        return jsonify(articles=articles_list, sort=sort_by)

    return render_template('wiki/search.html', 
                          articles=articles_list, 
                          query=query,
                          sort_by=sort_by,
                          categories=categories,
                          current_year=datetime.now().year,
                          seo=get_wiki_seo_settings('wiki'),
                          page_title=f"Search Results for '{query}' | Lusan's Wiki" if query else "Search | Lusan's Wiki",
                          page_description=f"Search results for '{query}' in technical documentation and programming tutorials" if query else "Search technical documentation and programming guides")


@wiki_bp.route('/article/<int:article_id>')
def article(article_id):
    article = WikiArticle.query.get_or_404(article_id)
    categories = get_categories()  # Get all top-level categories
    
    # Get next and previous articles
    prev_article = WikiArticle.query.filter(WikiArticle.id < article_id).order_by(WikiArticle.id.desc()).first()
    next_article = WikiArticle.query.filter(WikiArticle.id > article_id).order_by(WikiArticle.id.asc()).first()
    
    # Determine active category/subcategory
    active_category = None
    active_subcategory = None
    if article.category_id:
        category = WikiCategory.query.get(article.category_id)
        if category:
            if category.parent_id:
                active_subcategory = category.id
                active_category = category.parent_id
            else:
                active_category = category.id
    
    # Get SEO settings for the article
    seo = get_wiki_seo_settings('article')
    
    return render_template('wiki/article.html', 
                          article=article,
                          categories=categories,
                          prev_article=prev_article,
                          next_article=next_article,
                          active_category=active_category,
                          active_subcategory=active_subcategory,
                          current_year=datetime.now().year,
                          seo=seo,
                          page_title=seo.title if seo else article.title,
                          page_description=seo.meta_description if seo else article.summary)

@wiki_bp.route('/random')
def random():
    """Display random articles from the wiki."""
    all_articles = WikiArticle.query.all()
    categories = get_categories()
    
    if not all_articles:
        return render_template('wiki/not_found.html', 
                              message="No articles available yet.",
                              categories=categories,
                              current_year=datetime.now().year)
    
    # Get 6 random articles for the random page
    import random as py_random
    random_articles = py_random.sample(all_articles, min(len(all_articles), 6))
    
    return render_template('wiki/random_page.html', 
                          articles=random_articles,
                          categories=categories,
                          current_year=datetime.now().year,
                          seo=get_wiki_seo_settings('wiki'),
                          page_title="Random Articles | Lusan's Wiki",
                          page_description="Discover random technical articles and programming tutorials from the knowledge base")

@wiki_bp.route('/random-article')
def random_article():
    """Redirect to a single random article (for direct access)."""
    all_articles = WikiArticle.query.all()
    if not all_articles:
        return redirect(url_for('wiki.index'))
    
    import random as py_random
    random_article = py_random.choice(all_articles)
    return redirect(url_for('wiki.article', article_id=random_article.id))

@wiki_bp.route('/explore')
def explore():
    """Display all articles in a grid layout with filtering and sorting options."""
    categories = get_categories()
    
    # Get query parameters
    sort_by = request.args.get('sort', 'title')  # title, date, views
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 12  # Articles per page
    
    # Build base query
    query = WikiArticle.query
    
    # Apply category filter
    if category_filter and category_filter.isdigit():
        query = query.filter_by(category_id=int(category_filter))
    
    # Apply search filter
    if search_query:
        query = query.filter(
            or_(
                WikiArticle.title.ilike(f'%{search_query}%'),
                WikiArticle.summary.ilike(f'%{search_query}%'),
                WikiArticle.tags.ilike(f'%{search_query}%')
            )
        )
    
    # Apply sorting
    if sort_by == 'date':
        query = query.order_by(WikiArticle.created_at.desc())
    elif sort_by == 'views':
        query = query.order_by(WikiArticle.views.desc())
    else:  # title (default)
        query = query.order_by(WikiArticle.title.asc())
    
    # Paginate results
    articles_pagination = query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get all categories for filter dropdown
    all_categories = WikiCategory.query.all()
    
    return render_template('wiki/explore.html',
                          articles=articles_pagination.items,
                          pagination=articles_pagination,
                          categories=categories,
                          all_categories=all_categories,
                          sort_by=sort_by,
                          category_filter=category_filter,
                          search_query=search_query,
                          current_year=datetime.now().year,
                          seo=get_wiki_seo_settings('wiki'),
                          page_title="Explore Articles | Lusan's Wiki",
                          page_description="Browse and explore technical articles, programming tutorials, and development guides")