import os
import requests
import json

from flask import Blueprint, jsonify, request
from utils.ezyparts import EzyPartsError, get_client
from utils.vehicle_parser import parse_vehicle_response
from utils.google_places import GooglePlacesClient, GooglePlacesError

api_main_bp = Blueprint('api_main', __name__, url_prefix='/api')

@api_main_bp.route('/lookup-rego', methods=['POST'])
def lookup_rego():
    """Lookup vehicle by registration from EzyParts"""
    rego = request.form.get('rego') or request.json.get('rego', '')
    state = request.form.get('state') or request.json.get('state', '')
    
    if not rego:
        return jsonify({'error': 'Registration number required'}), 400
    
    if not state:
        return jsonify({'error': 'Registration state required'}), 400
    
    try:
        client = get_client()
        rego_data = client.lookup_rego(rego, state)
        
        if not rego_data:
            return jsonify({'error': 'No vehicles found'}), 404

        # Parse for variant selection
        parsed = parse_vehicle_response(rego_data)
        
        if not parsed:
            return jsonify({'error': 'Could not parse vehicle data'}), 500
        
        return jsonify(parsed)
        
    except EzyPartsError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': f'Lookup failed: {str(e)}'}), 500

@api_main_bp.route("/address-autocomplete", methods=["GET"])
def address_autocomplete():
    """Proxy for Google Places Autocomplete API with postcode support"""
    
    query = request.args.get("q") or request.args.get("query") or ""
    
    if not query and request.is_json:
        query = request.json.get("query", "")
    elif not query and request.form:
        query = request.form.get("query", "")
    
    if not query or len(query) < 3:
        return jsonify({"error": "Query parameter required (minimum 3 characters)"}), 400
    
    api_key = os.environ.get('GOOGLE_PLACES_API_KEY')
    if not api_key:
        return jsonify({"error": "Google Places API key not configured"}), 500
    
    try:
        client = GooglePlacesClient(api_key=api_key)

        suggestions = client.autocomplete_address(query)
        
        return jsonify({
            "status": "success",
            "suggestions": suggestions,
            "location_bias": {
                "center": "Canberra, ACT",
                "radius_km": 50
            }
        })
        
    except requests.RequestException as e:
        return jsonify({"error": f"Address lookup failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500