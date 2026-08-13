from functools import wraps
from flask import session, redirect, url_for # pyright: ignore[reportMissingImports]

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in_admin'):
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated