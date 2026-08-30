from flask import Blueprint, jsonify, request
from extensions import db
from models import Customer

api_customers_bp = Blueprint('api_customers', __name__, url_prefix='/api/customers')


@api_customers_bp.route('/search')
def search_customers():
    """Search customers - returns JSON"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify([])
    
    # Split into terms for multi-word search
    terms = query.split()
    
    conditions = []
    for term in terms:
        search_pattern = f'%{term}%'
        conditions.append(
            db.or_(
                Customer.first_name.ilike(search_pattern),
                Customer.last_name.ilike(search_pattern),
                db.func.concat(Customer.first_name, ' ', Customer.last_name).ilike(search_pattern),
                Customer.email.ilike(search_pattern),
                Customer.phone.ilike(search_pattern),
                Customer.mobile.ilike(search_pattern),
                Customer.company_name.ilike(search_pattern)
            )
        )
    
    customers = Customer.query.filter(*conditions).limit(limit).all()
    
    results = [{
        'id': c.id,
        'name': c.full_name,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'email': c.email or '',
        'phone': c.phone or '',
        'mobile': c.mobile or '',
        'company': c.company_name or '',
        'address': c.address or '',
        'city': c.city or '',
        'state': c.state or ''
    } for c in customers]
    
    return jsonify(results)


@api_customers_bp.route('/<int:customer_id>')
def get_customer(customer_id):
    """Get customer by ID - returns JSON"""
    customer = Customer.query.get_or_404(customer_id)
    
    return jsonify({
        'id': customer.id,
        'name': customer.full_name,
        'first_name': customer.first_name,
        'last_name': customer.last_name,
        'email': customer.email or '',
        'phone': customer.phone or '',
        'mobile': customer.mobile or '',
        'company': customer.company_name or '',
        'address': customer.address or '',
        'city': customer.city or '',
        'state': customer.state or '',
        'postal_code': customer.postal_code or '',
        'country': customer.country or '',
        'vehicle_count': customer.vehicle_count
    })


@api_customers_bp.route('/<int:customer_id>/vehicles')
def get_customer_vehicles(customer_id):
    """Get all vehicles for a customer - returns JSON"""
    customer = Customer.query.get_or_404(customer_id)
    vehicles = customer.vehicles.all()
    
    results = [{
        'id': v.id,
        'registration_no': v.registration_no,
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'fuel_type': v.fuel_type,
        'transmission': v.transmission,
        'odometer_reading': v.odometer_reading
    } for v in vehicles]
    
    return jsonify(results)