from flask import Blueprint, render_template
from models import Customer, Vehicle

admin_dashboard_bp = Blueprint('admin_dashboard', __name__, url_prefix='/admin')


@admin_dashboard_bp.route('/')
def dashboard():
    total_customers = Customer.query.count()
    total_vehicles = Vehicle.query.count()
    recent_customers = Customer.query.order_by(Customer.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_customers=total_customers,
                         total_vehicles=total_vehicles,
                         recent_customers=recent_customers)
