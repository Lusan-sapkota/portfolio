from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models import WikiArticle, WikiCategory
from database import db
from sqlalchemy import or_
from . import wiki_bp
from datetime import datetime
import random

# Helper function to get all top-level categories
def get_categories():
    return WikiCategory.query.filter_by(parent_id=None).all()

@wiki_bp.route('/')
def index():
    print(f"DEBUG: Accessing wiki blueprint index route.")
    articles = WikiArticle.query.order_by(WikiArticle.title).all()
    categories = get_categories()
    
    # Convert categories to dictionaries with article counts
    categories_with_counts = []
    for category in categories:
        category_dict = {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'article_count': WikiArticle.query.filter_by(category_id=category.id).count(),
            'subcategories': category.subcategories if hasattr(category, 'subcategories') else []
        }
        categories_with_counts.append(category_dict)
    
    return render_template('wiki/index.html', 
                          articles=articles, 
                          categories=categories_with_counts,
                          active_category=None,
                          active_subcategory=None,
                          current_year=datetime.now().year)

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
                          current_year=datetime.now().year)


@wiki_bp.route('/article/<int:article_id>')
def article(article_id):
    article = WikiArticle.query.get_or_404(article_id)
    categories = get_categories()  # Get all top-level categories
    
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
    
    return render_template('wiki/article.html', 
                          article=article,
                          categories=categories,
                          active_category=active_category,
                          active_subcategory=active_subcategory,
                          current_year=datetime.now().year)

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
                          current_year=datetime.now().year)

@wiki_bp.route('/random-article')
def random_article():
    """Redirect to a single random article (for direct access)."""
    all_articles = WikiArticle.query.all()
    if not all_articles:
        return redirect(url_for('wiki.index'))
    
    import random as py_random
    random_article = py_random.choice(all_articles)
    return redirect(url_for('wiki.article', article_id=random_article.id))