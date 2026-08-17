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
    phone = request.args.get('phone')
    email = request.args.get('email')
    customers = Customer.query.order_by(Customer.created_at.desc())
    if phone:
        customers = customers.filter_by(phone = phone)
    if email:
        customers = customers.filter_by(email = email)
    customers = customers.all()
    return jsonify([c.to_dict() for c in customers])

@api_bp.route('/customers/create', methods=['POST'])
@login_required
def api_customer_create():

    print(request.get_json())

    first_name = request.get_json().get('first_name')
    last_name = request.get_json().get('last_name')
    phone = request.get_json().get('phone')
    email = request.get_json().get('email')
    street = request.get_json().get('street')
    suburb = request.get_json().get('suburb')
    state = request.get_json().get('state')
    postcode = request.get_json().get('postcode')

    customer = Customer(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        street=street,
        suburb=suburb,
        state=state,
        postcode=postcode
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict())
    # return jsonify({'ok': True, 'message': 'Customer creation endpoint is under construction.'}), 200

@api_bp.route('/vehicles/search')
@login_required
def api_vehicle_search():
    rego = request.args.get('rego')
    vin = request.args.get('vin')

    vehicles = Vehicle.query.order_by(Vehicle.created_at.desc())
    if rego:
        vehicles = vehicles.filter_by(rego = rego)
    if vin:
        vehicles = vehicles.filter_by(vin = vin)

    vehicles = vehicles.all()
    return jsonify([v.to_dict() for v in vehicles])

@api_bp.route('/vehicles/create', methods=['POST'])
@login_required
def api_vehicle_create():

    make = request.get_json().get('make')
    model = request.get_json().get('model')
    series = request.get_json().get('series')
    year = request.get_json().get('year')
    rego = request.get_json().get('rego')
    rego_state = request.get_json().get('rego_state')
    vin = request.get_json().get('vin')

    vehicle = Vehicle(
        make=make,
        model=model,
        series=series,
        year=year,
        rego=rego,
        rego_state=rego_state,
        vin=vin
    )
    db.session.add(vehicle)
    db.session.commit()

    return jsonify(vehicle.to_dict())
