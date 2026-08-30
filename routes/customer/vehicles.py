from flask import Blueprint, render_template
from models import Vehicle

customer_vehicles_bp = Blueprint('customer_vehicles', __name__, url_prefix='/customer/vehicles')


@customer_vehicles_bp.route('/')
def my_vehicles():
    vehicles = Vehicle.query.limit(5).all()
    return render_template('customer/vehicles.html', vehicles=vehicles)
