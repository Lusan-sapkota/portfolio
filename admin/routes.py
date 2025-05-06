from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

admin_bp = Blueprint('admin', __name__, template_folder='templates')

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('You need to be logged in as admin to access this page.')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Replace with proper authentication
        if username == 'admin' and password == 'password':
            session['admin'] = True
            return redirect(url_for('admin.index'))
        flash('Invalid credentials')
    return render_template('admin/login.html')

@admin_bp.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))