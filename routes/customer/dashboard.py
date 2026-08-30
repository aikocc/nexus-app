from flask import Blueprint, render_template
from models import Customer

customer_dashboard_bp = Blueprint('customer_dashboard', __name__, url_prefix='/customer')


@customer_dashboard_bp.route('/')
def dashboard():
    customer = Customer.query.first()
    vehicles = customer.vehicles.all() if customer else []
    return render_template('customer/dashboard.html', 
                         customer=customer, 
                         vehicles=vehicles)
