from flask import Blueprint, request, session, redirect, render_template, flash, url_for # pyright: ignore[reportMissingImports]
from os import environ

auth_bp = Blueprint("auth", __name__, url_prefix="")

ADMIN_USERNAME = environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD', 'nexus2026')


@auth_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if (request.form.get('username') == ADMIN_USERNAME and
                request.form.get('password') == ADMIN_PASSWORD):
            session['logged_in_admin'] = True
            return redirect(url_for('admin_dashboard.admin_dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('admin_login.html')


@auth_bp.route('/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

