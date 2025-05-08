from flask import render_template, request, redirect, url_for, flash, jsonify
from functools import wraps
from models import User
from . import admin_bp
from database import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, unset_jwt_cookies 

# Admin required decorator using JWT
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or not user.is_admin:
            return jsonify(msg="Admins only!"), 403 # Or redirect to login
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def index():
    # This route is now protected by JWT and admin check
    return render_template('admin/index.html') # Assuming you have admin/index.html

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form # Or request.get_json() if you switch to JSON requests
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('admin/login.html'), 400 # Or jsonify error

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_admin:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                # For a form submission, redirecting and setting cookies might be one way,
                # but typically JWTs are returned in JSON for SPAs.
                # For now, returning JSON. Frontend needs to handle this.
                response = jsonify({
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token
                })
                # If you want to set cookies (HttpOnly for security):
                # from flask_jwt_extended import set_access_cookies, set_refresh_cookies
                # set_access_cookies(response, access_token)
                # set_refresh_cookies(response, refresh_token)
                # return response, 200
                return response, 200
            else:
                flash('User is not an admin.', 'warning')
        else:
            flash('Invalid username or password.', 'danger')
        
        # If login fails, re-render login page with flash message
        # If you switch to full AJAX, this part changes.
        return render_template('admin/login.html'), 401

    # For GET request, just render the login page
    return render_template('admin/login.html')


@admin_bp.route('/logout', methods=['POST']) # Changed to POST, more appropriate for logout
@jwt_required() # Protect logout, ensure user is logged in
def logout():
    # For JWT, logout typically means the client discards the token.
    # To implement server-side logout (token blocklisting), you'd need more setup.
    # This example provides a basic response.
    # If using cookies, you can unset them:
    # response = jsonify({'message': 'Logout successful'})
    # unset_jwt_cookies(response)
    # return response, 200
    return jsonify(message="Logout successful. Please clear your tokens."), 200

@admin_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True) # Requires a valid refresh token
def refresh():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token), 200

# ... rest of your admin routes, ensure they use @admin_required