from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app
from models import WikiArticle, WikiCategory  # Add WikiCategory import
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
    
    return render_template('wiki/index.html', 
                          articles=articles, 
                          categories=categories,
                          active_category=None,
                          active_subcategory=None,
                          current_year=datetime.now().year)

@wiki_bp.route('/search')
def search():
    query = request.args.get('q', '')
    articles_list = []
    categories = get_categories()  # Get all top-level categories

    if query:
        articles_query = WikiArticle.query.filter(
            or_(
                WikiArticle.title.ilike(f'%{query}%'),
                WikiArticle.content.ilike(f'%{query}%'),
                WikiArticle.tags.ilike(f'%{query}%')
            )
        ).all()
        articles_list = [article.to_dict() for article in articles_query]

    if request.accept_mimetypes.accept_json and \
       not request.accept_mimetypes.accept_html:
        return jsonify(articles=articles_list)

    return render_template('wiki/search.html', 
                          articles=articles_list, 
                          query=query,
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
def random():  # Change from 'random_article' to 'random'
    """Display a random article from the wiki."""
    articles = WikiArticle.query.all()
    if not articles:
        return render_template('wiki/not_found.html', 
                              message="No articles available yet.",
                              categories=get_categories(),
                              current_year=datetime.now().year)
    
    random_article = random.choice(articles)
    return redirect(url_for('wiki.article', article_id=random_article.id))