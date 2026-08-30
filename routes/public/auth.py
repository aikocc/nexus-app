from flask import Blueprint, render_template
from forms.public.auth_forms import LoginForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login')
def login():
    form = LoginForm()
    return render_template('public/login.html', form=form)


@auth_bp.route('/register')
def register():
    return render_template('public/register.html')


@auth_bp.route('/logout')
def logout():
    return render_template('public/index.html')
