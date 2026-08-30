from flask import Blueprint, jsonify, request
from extensions import db
from models import Vehicle

api_vehicles_bp = Blueprint('api_vehicles', __name__, url_prefix='/api/vehicles')


@api_vehicles_bp.route('/search')
def search_vehicles():
    """Search vehicles - returns JSON"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    
    if not query:
        return jsonify([])
    
    search_pattern = f'%{query}%'
    vehicles = Vehicle.query.filter(
        db.or_(
            Vehicle.registration_no.ilike(search_pattern),
            Vehicle.vin.ilike(search_pattern),
            Vehicle.make.ilike(search_pattern),
            Vehicle.model.ilike(search_pattern)
        )
    ).limit(limit).all()
    
    results = [{
        'id': v.id,
        'registration_no': v.registration_no,
        'vin': v.vin or '',
        'make': v.make,
        'model': v.model,
        'year': v.year,
        'fuel_type': v.fuel_type or '',
        'transmission': v.transmission or '',
        'customer_id': v.customer_id,
        'customer_name': v.customer.full_name if v.customer else ''
    } for v in vehicles]
    
    return jsonify(results)


@api_vehicles_bp.route('/<int:vehicle_id>')
def get_vehicle(vehicle_id):
    """Get vehicle by ID - returns JSON"""
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    
    return jsonify({
        'id': vehicle.id,
        'customer_id': vehicle.customer_id,
        'customer_name': vehicle.customer.full_name if vehicle.customer else '',
        'registration_no': vehicle.registration_no,
        'rego_state': vehicle.rego_state or '',
        'vin': vehicle.vin or '',
        'make': vehicle.make,
        'model': vehicle.model,
        'sub_model': vehicle.sub_model or '',
        'series': vehicle.series or '',
        'year': vehicle.year,
        'body_type': vehicle.body_type or '',
        'drive_type': vehicle.drive_type or '',
        'fuel_type': vehicle.fuel_type or '',
        'transmission': vehicle.transmission or '',
        'engine_spec': vehicle.engine_spec or '',
        'chassis_no': vehicle.chassis_no or '',
        'color': vehicle.color or '',
        'odometer_reading': vehicle.odometer_reading,
        'notes': vehicle.notes or ''
    })