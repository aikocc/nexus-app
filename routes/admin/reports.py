from flask import Blueprint, render_template
from models import Customer, Vehicle

admin_reports_bp = Blueprint('admin_reports', __name__, url_prefix='/admin/reports')


@admin_reports_bp.route('/')
def reports_dashboard():
    total_customers = Customer.query.count()
    total_vehicles = Vehicle.query.count()
    
    return render_template('admin/reports.html',
                         total_customers=total_customers,
                         total_vehicles=total_vehicles)
