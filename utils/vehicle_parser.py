"""
Vehicle Registration Data Parser
Parses ACT Rego Search API responses.
Returns all variants for user selection, then only saves selected variant.
"""
import json
import re


def parse_vehicle_response(response_data):
    """Parse rego search response and return all variants for user selection"""
    
    vehicles = extract_vehicles(response_data)
    
    if not vehicles:
        return None
    
    common_fields = extract_common_fields(response_data, vehicles)
    
    variants = []
    for v in vehicles:
        details = v.get('details', '') or v.get('lngDsc', '')
        model_parts = v.get('model', '').split(',')
        
        variant = {
            'id': v.get('id'),
            'make': v.get('make') or common_fields.get('make'),
            'model': model_parts[0].strip() if model_parts else '',
            'sub_model': model_parts[1].strip() if len(model_parts) > 1 else v.get('subModel'),
            'series': v.get('series'),
            'year': parse_compliance_year(
                v.get('year') or 
                common_fields.get('complianceDate') or 
                response_data.get('year')
            ),
            'body_type': parse_body_type(details),
            'drive_type': parse_drive_type(details),
            'fuel_type': parse_fuel_type(v.get('engine', '')),
            'transmission': parse_transmission(details),
            'engine_spec': v.get('engine'),
            'chassis_no': v.get('seriesChassis') or v.get('chassis'),
            'doors': parse_doors(details),
            'details': details.strip(),
            'description': build_variant_description(v, details)
        }
        
        variants.append(variant)

    print(json.dumps({
        'data': response_data,
        'common': common_fields,
        'variants': variants,
        'variant_count': len(variants)
    }, indent=4))
    
    return {
        'common': common_fields,
        'variants': variants,
        'variant_count': len(variants)
    }


def extract_vehicles(response_data):
    """Extract vehicles list from various response structures"""
    
    vehicles = []
    
    # Check 'vehicle' key first
    if 'vehicle' in response_data and isinstance(response_data['vehicle'], dict):
        vehicle_data = response_data['vehicle']
        raw_vehicles = vehicle_data.get('vehicles', [])
        
        if isinstance(raw_vehicles, list) and raw_vehicles:
            # Check if double-nested
            if isinstance(raw_vehicles[0], dict) and 'vehicles' in raw_vehicles[0]:
                vehicles = raw_vehicles[0]['vehicles']
            else:
                vehicles = raw_vehicles
    
    # Fallback: check top-level 'vehicles'
    if not vehicles and 'vehicles' in response_data:
        raw_vehicles = response_data.get('vehicles', [])
        if isinstance(raw_vehicles, list) and raw_vehicles:
            if isinstance(raw_vehicles[0], dict) and 'vehicles' in raw_vehicles[0]:
                vehicles = raw_vehicles[0]['vehicles']
            else:
                vehicles = raw_vehicles
    
    return vehicles


def extract_common_fields(response_data, vehicles):
    """Extract common fields from various response structures"""
    
    common = {
        'registration_no': None,
        'rego_state': None,
        'vin': None,
        'make': None,
        'complianceDate': None,
    }
    
    # Check 'registration' key first (most authoritative)
    if 'registration' in response_data and isinstance(response_data['registration'], dict):
        reg = response_data['registration']
        common['registration_no'] = reg.get('rego')
        common['rego_state'] = reg.get('regoState')
        common['vin'] = reg.get('vin')
        common['make'] = reg.get('make')
        common['complianceDate'] = reg.get('complianceDate') or reg.get('year')
    
    # Check 'vehicle' key
    if 'vehicle' in response_data and isinstance(response_data['vehicle'], dict):
        veh = response_data['vehicle']
        if not common['registration_no']:
            common['registration_no'] = veh.get('rego')
        if not common['rego_state']:
            common['rego_state'] = veh.get('regoState')
        if not common['vin']:
            common['vin'] = veh.get('vin')
        if not common['make']:
            common['make'] = veh.get('make')
        if not common['complianceDate']:
            common['complianceDate'] = veh.get('complianceDate') or veh.get('year')
    
    # Check top level
    if not common['registration_no']:
        common['registration_no'] = response_data.get('rego')
    if not common['rego_state']:
        common['rego_state'] = response_data.get('regoState')
    if not common['vin']:
        common['vin'] = response_data.get('vin')
    if not common['make']:
        common['make'] = response_data.get('make')
    if not common['complianceDate']:
        common['complianceDate'] = response_data.get('complianceDate') or response_data.get('year')
    
    # Check first vehicle as fallback
    if vehicles and isinstance(vehicles, list) and vehicles:
        first = vehicles[0]
        if not common['registration_no'] and first.get('rego'):
            common['registration_no'] = first.get('rego')
        if not common['rego_state'] and first.get('regoState'):
            common['rego_state'] = first.get('regoState')
        if not common['vin'] and first.get('vin'):
            common['vin'] = first.get('vin')
        if not common['make'] and first.get('make'):
            common['make'] = first.get('make')
    
    return common


def build_variant_description(vehicle, details):
    """Build a human-readable description for the variant"""
    parts = []
    
    model_parts = vehicle.get('model', '').split(',')
    if model_parts and model_parts[0].strip():
        parts.append(model_parts[0].strip())
    if len(model_parts) > 1 and model_parts[1].strip():
        parts.append(model_parts[1].strip())
    elif vehicle.get('subModel'):
        parts.append(vehicle['subModel'])
    
    if vehicle.get('engine'):
        engine = vehicle['engine']
        size_match = re.search(r'(\d+\.\d+L)', engine)
        if size_match:
            parts.append(size_match.group(1))
    
    if vehicle.get('year'):
        parts.append(f"({vehicle['year']})")
    
    return " ".join(parts) if parts else vehicle.get('desc', '')


def selected_variant_to_vehicle(selected_variant, common_fields):
    """Convert selected variant + common fields into database-ready dict"""
    
    return {
        'registration_no': common_fields.get('registration_no'),
        'rego_state': common_fields.get('rego_state'),
        'vin': common_fields.get('vin'),
        'make': selected_variant.get('make'),
        'model': selected_variant.get('model'),
        'sub_model': selected_variant.get('sub_model'),
        'series': selected_variant.get('series'),
        'year': selected_variant.get('year'),
        'body_type': selected_variant.get('body_type'),
        'drive_type': selected_variant.get('drive_type'),
        'fuel_type': selected_variant.get('fuel_type'),
        'transmission': selected_variant.get('transmission'),
        'engine_spec': selected_variant.get('engine_spec'),
        'chassis_no': selected_variant.get('chassis_no'),
        'doors': selected_variant.get('doors'),
    }


def parse_compliance_year(year_str):
    """Extract compliance year from various formats"""
    if not year_str:
        return None
    
    year_str = str(year_str)
    
    if '~' in year_str:
        match = re.search(r'(\d{4})', year_str.split('~')[0])
        return int(match.group(1)) if match else None
    
    month_year = re.search(r'(\d{2})/(\d{4})', year_str)
    if month_year:
        return int(month_year.group(2))
    
    year_month = re.search(r'(\d{4})-(\d{2})', year_str)
    if year_month:
        return int(year_month.group(1))
    
    match = re.search(r'(\d{4})', year_str)
    return int(match.group(1)) if match else None


def parse_body_type(details):
    """Extract body type from details string"""
    if not details:
        return None
    
    body_map = {
        'Sedan': ['Sedan'],
        'SUV': ['SUV'],
        'Ute': ['Ute', 'Utility'],
        'Hatchback': ['Hatch'],
        'Wagon': ['Wagon'],
        'Convertible': ['Convertible'],
        'Coupe': ['Coupe'],
        'Van': ['Van'],
        'Minibus': ['Minibus'],
        'Truck': ['Truck'],
        'Commercial': ['Commercial']
    }
    
    for body, keywords in body_map.items():
        if any(kw in details for kw in keywords):
            return body
    return None


def parse_doors(details):
    """Extract door count from details string"""
    if not details:
        return None
    
    if '4D' in details or '4 Door' in details:
        return 4
    elif '3D' in details or '3 Door' in details:
        return 3
    elif '2D' in details or '2 Door' in details:
        return 2
    elif '5D' in details or '5 Door' in details:
        return 5
    return None


def parse_drive_type(details):
    """Extract drive type from details string"""
    if not details:
        return None
    
    if 'FWD' in details:
        return 'FWD'
    elif 'RWD' in details:
        return 'RWD'
    elif 'AWD' in details:
        return 'AWD'
    elif '4WD' in details:
        return '4WD'
    elif '2WD' in details:
        return '2WD'
    return None


def parse_fuel_type(engine):
    """Extract fuel type from engine string"""
    if not engine:
        return None
    
    engine_upper = engine.upper()
    
    if 'BEV' in engine_upper or 'ELECTRIC' in engine_upper:
        return 'BEV'
    elif 'PHEV' in engine_upper or 'PLUG-IN' in engine_upper:
        return 'PHEV'
    elif 'HYB' in engine_upper or 'HYBRID' in engine_upper:
        return 'HYBRID'
    elif 'DIE' in engine_upper or 'DIESEL' in engine_upper:
        return 'DIESEL'
    elif 'PET' in engine_upper or 'PETROL' in engine_upper:
        return 'PETROL'
    elif 'LPG' in engine_upper:
        return 'LPG'
    return None


def parse_transmission(details):
    """Extract transmission from details string"""
    if not details:
        return None
    
    if 'AT/MT' in details or 'Auto or Manual' in details or 'AMT' in details:
        return 'Auto/Manual'
    elif 'Auto' in details:
        return 'Auto'
    elif 'Manual' in details:
        return 'Manual'
    elif 'CVT' in details:
        return 'CVT'
    elif 'AT' in details:
        return 'Auto'
    elif 'MT' in details:
        return 'Manual'
    return None