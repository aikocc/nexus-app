from flask import Blueprint, render_template

services_bp = Blueprint('services', __name__, url_prefix='/services')


@services_bp.route('/')
def service_list():
    services = [
        {'name': 'Oil Change', 'price': '$49.99', 'duration': '30 min'},
        {'name': 'Brake Service', 'price': '$199.99', 'duration': '2 hours'},
        {'name': 'Tire Rotation', 'price': '$29.99', 'duration': '30 min'},
        {'name': 'Full Diagnostic', 'price': '$89.99', 'duration': '1 hour'},
    ]
    return render_template('public/services.html', services=services)
