from flask import Blueprint, render_template, request, redirect, url_for, current_app, jsonify
from . import notespark_bp

@notespark_bp.route('/')
def index():
    """Render the main Notespark page"""
    print("DEBUG: Accessing Notespark blueprint index route. Attempting to render 'notespark/index.html'")
    
    # Render the main page template
    return render_template('notespark/index.html')

@notespark_bp.route('/releases')
def releases():
    """Render the releases & changelog page"""
    print("DEBUG: Accessing Notespark releases route. Attempting to render 'notespark/releases.html'")
    return render_template('notespark/releases.html')

@notespark_bp.route('/download')
def download():
    """Render the download page"""
    print("DEBUG: Accessing Notespark download route. Attempting to render 'notespark/download.html'")
    return render_template('notespark/download.html')

@notespark_bp.route('/docs')
def docs():
    """Render the documentation page"""
    print("DEBUG: Accessing Notespark docs route. Attempting to render 'notespark/docs.html'")
    return render_template('notespark/docs.html')

@notespark_bp.route('/about')
def about():
    """Render the about page"""
    print("DEBUG: Accessing Notespark about route. Attempting to render 'notespark/about.html'")
    return render_template('notespark/about.html')