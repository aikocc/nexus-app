from database import db, Booking, Lead, Customer, Vehicle
from decorators import login_required

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # pyright: ignore[reportMissingImports]

api_bp = Blueprint("api", __name__, url_prefix="/api", template_folder='templates')

@api_bp.route('/bookings')
@login_required
def api_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bookings])

@api_bp.route('/bookings')
@login_required
def api_leads():
    leads = Lead.query.order_by(Lead.created_at.desc()).all()
    return jsonify([l.to_dict() for l in leads])

@api_bp.route('/customers/search')
@login_required
def api_customer_search():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers])

@api_bp.route('/customers/create')
@login_required
def api_customer_create():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers])

@api_bp.route('/vehicles/search')
@login_required
def api_vehicle_search():
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return jsonify([v.to_dict() for v in vehicles])