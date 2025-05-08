from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app # Added current_app
from models import WikiArticle
from database import db
from sqlalchemy import or_
from . import wiki_bp

@wiki_bp.route('/')
def index():
    print(f"DEBUG: Accessing wiki blueprint index route. Attempting to render 'wiki/index.html'") # Updated log
    articles = WikiArticle.query.order_by(WikiArticle.title).all()

    template_name_to_render = 'wiki/index.html' # Changed
    jinja_env = current_app.jinja_env
    try:
        template_object = jinja_env.get_template(template_name_to_render)
        print(f"DEBUG: Jinja2 resolved '{template_name_to_render}' to file: {template_object.filename}")
    except Exception as e:
        print(f"DEBUG: Error getting template '{template_name_to_render}' from Jinja2 env: {e}")

    return render_template(template_name_to_render, articles=articles) # Changed

@wiki_bp.route('/search')
def search():
    query = request.args.get('q', '')
    articles_list = []

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

    # Also update search.html if it's in wiki/templates
    return render_template('wiki/search.html', articles=articles_list, query=query) # Assuming search.html is in wiki/templates


@wiki_bp.route('/article/<int:article_id>')
def article(article_id):
    article = WikiArticle.query.get_or_404(article_id)
    # Also update article.html if it's in wiki/templates
    return render_template('wiki/article.html', article=article) # Assuming article.html is in wiki/templates