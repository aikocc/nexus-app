from database import db, Booking, Lead, Customer, Vehicle
from decorators import login_required

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # pyright: ignore[reportMissingImports]

api_bp = Blueprint("api", __name__, url_prefix="/api", template_folder='templates')

@api_bp.route('/bookings')
@login_required
def api_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return jsonify([b.to_dict() for b in bookings])

@api_bp.route('/leads')
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

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    street = request.form.get('street')
    suburb = request.form.get('suburb')
    state = request.form.get('state')
    postcode = request.form.get('postcode')

    return jsonify([0,])
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return jsonify([c.to_dict() for c in customers])

@api_bp.route('/vehicles/search')
@login_required
def api_vehicle_search():
    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc()).all()
    return jsonify([v.to_dict() for v in vehicles])

@api_bp.route('/vehicles/create')
@login_required
def api_vehicle_create():

    make = request.form.get('make')
    model = request.form.get('model')
    series = request.form.get('series')
    year = request.form.get('year')
    rego = request.form.get('rego')
    rego_state = request.form.get('rego_state')
    vin = request.form.get('vin')

    

    return jsonify([0,])
