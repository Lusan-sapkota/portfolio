from flask import redirect
from . import store_bp

@store_bp.route('/')
def index():
    """
    Redirect to the main store page.
    """
    return redirect("https://store.lusansapkota.com.np")