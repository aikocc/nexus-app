# # seed_data.py
# from datetime import datetime, timedelta, timezone
# from extensions import db
# from models import Customer, Vehicle, Lead, Booking
# import random

# # Use this helper function for current UTC time
# def utc_now():
#     """Get current UTC datetime with timezone awareness"""
#     return datetime.now(timezone.utc)

# def utc_today():
#     """Get today's date in UTC"""
#     return utc_now().date()

# def seed_database():
#     """Populate database with seed data"""
    
#     print("Clearing existing data...")
#     # Clear existing data (optional - use with caution)
#     Booking.query.delete()
#     Lead.query.delete()
#     Vehicle.query.delete()
#     Customer.query.delete()
#     db.session.commit()
    
#     print("Creating customers...")
#     customers = []
    
#     # Individual customers
#     individual_customers = [
#         {
#             'first_name': 'John', 'last_name': 'Smith', 
#             'email': 'john.smith@gmail.com', 'phone': '0412345678',
#             'mobile': '0412345678', 'address': '123 Main St', 
#             'city': 'Sydney', 'state': 'NSW', 'postal_code': '2000',
#             'country': 'Australia', 'is_company': False, 
#             'notes': 'Prefers morning appointments'
#         },
#         {
#             'first_name': 'Sarah', 'last_name': 'Johnson', 
#             'email': 'sarah.j@outlook.com', 'phone': '0423456789',
#             'mobile': '0423456789', 'address': '456 Beach Rd', 
#             'city': 'Melbourne', 'state': 'VIC', 'postal_code': '3000',
#             'country': 'Australia', 'is_company': False,
#             'notes': 'Has multiple vehicles'
#         },
#         {
#             'first_name': 'Michael', 'last_name': 'Brown', 
#             'email': 'michael.brown@hotmail.com', 'phone': '0434567890',
#             'mobile': '0434567890', 'address': '789 Park Ave', 
#             'city': 'Brisbane', 'state': 'QLD', 'postal_code': '4000',
#             'country': 'Australia', 'is_company': False,
#             'notes': 'Interested in fleet discounts'
#         },
#         {
#             'first_name': 'Emily', 'last_name': 'Davis', 
#             'email': 'emily.davis@gmail.com', 'phone': '0445678901',
#             'mobile': '0445678901', 'address': '321 Hill St', 
#             'city': 'Perth', 'state': 'WA', 'postal_code': '6000',
#             'country': 'Australia', 'is_company': False,
#             'notes': ''
#         },
#         {
#             'first_name': 'David', 'last_name': 'Wilson', 
#             'email': 'david.wilson@yahoo.com', 'phone': '0456789012',
#             'mobile': '0456789012', 'address': '654 Valley Rd', 
#             'city': 'Adelaide', 'state': 'SA', 'postal_code': '5000',
#             'country': 'Australia', 'is_company': False,
#             'notes': 'Prefers SMS communication'
#         },
#     ]
    
#     # Company customers
#     company_customers = [
#         {
#             'first_name': 'Robert', 'last_name': 'Taylor', 
#             'company_name': 'Taylor Transport Pty Ltd',
#             'email': 'robert.taylor@taylortransport.com.au', 
#             'phone': '0467890123',
#             'mobile': '0467890123', 'address': '987 Industrial Dr', 
#             'city': 'Sydney', 'state': 'NSW', 'postal_code': '2145',
#             'country': 'Australia', 'is_company': True,
#             'notes': 'Fleet account - 5 vehicles',
#             'tax_id': 'ABN 12 345 678 901'
#         },
#         {
#             'first_name': 'Jennifer', 'last_name': 'Martinez',
#             'company_name': 'Martinez Auto Group',
#             'email': 'jen@martinezautogroup.com.au', 
#             'phone': '0478901234',
#             'mobile': '0478901234', 'address': '234 Showroom Blvd', 
#             'city': 'Melbourne', 'state': 'VIC', 'postal_code': '3150',
#             'country': 'Australia', 'is_company': True,
#             'notes': 'Vehicle reseller - needs quick turnaround',
#             'tax_id': 'ABN 98 765 432 109'
#         },
#         {
#             'first_name': 'James', 'last_name': 'Anderson',
#             'company_name': 'Anderson Fleet Services',
#             'email': 'james.anderson@afs.com.au', 
#             'phone': '0489012345',
#             'mobile': '0489012345', 'address': '567 Logistics Way', 
#             'city': 'Brisbane', 'state': 'QLD', 'postal_code': '4008',
#             'country': 'Australia', 'is_company': True,
#             'notes': 'Corporate account - monthly service',
#             'tax_id': 'ABN 56 789 012 345'
#         },
#     ]
    
#     all_customer_data = individual_customers + company_customers
    
#     for data in all_customer_data:
#         customer = Customer(**data)
#         db.session.add(customer)
#         customers.append(customer)
    
#     db.session.commit()
#     print(f"Created {len(customers)} customers")
    
#     print("Creating vehicles...")
    
#     # Vehicle definitions (mapped to customer indices)
#     vehicle_definitions = [
#         # Customer 1: John Smith (index 0) - 2 vehicles
#         {
#             'customer_id': customers[0].id,
#             'registration_no': 'ABC123',
#             'rego_state': 'NSW',
#             'vin': '1HGCM82633A123456',
#             'make': 'Honda',
#             'model': 'Civic',
#             'sub_model': 'VTi-S',
#             'year': 2020,
#             'body_type': 'Sedan',
#             'fuel_type': 'Petrol',
#             'transmission': 'Automatic',
#             'color': 'Silver',
#             'odometer_reading': 45000,
#             'notes': 'Regular service due'
#         },
#         {
#             'customer_id': customers[0].id,
#             'registration_no': 'XYZ789',
#             'rego_state': 'NSW',
#             'vin': '5FNRL3H55BB123456',
#             'make': 'Toyota',
#             'model': 'Corolla',
#             'sub_model': 'Ascent Sport',
#             'year': 2018,
#             'body_type': 'Hatchback',
#             'fuel_type': 'Petrol',
#             'transmission': 'CVT',
#             'color': 'White',
#             'odometer_reading': 78000,
#             'notes': ''
#         },
#         # Customer 2: Sarah Johnson (index 1) - 3 vehicles
#         {
#             'customer_id': customers[1].id,
#             'registration_no': 'DEF456',
#             'rego_state': 'VIC',
#             'vin': 'WDDGF4HB7CG123456',
#             'make': 'Mercedes-Benz',
#             'model': 'C200',
#             'sub_model': 'Avantgarde',
#             'year': 2019,
#             'body_type': 'Sedan',
#             'fuel_type': 'Diesel',
#             'transmission': 'Automatic',
#             'color': 'Black',
#             'odometer_reading': 32000,
#             'notes': 'Premium service required'
#         },
#         {
#             'customer_id': customers[1].id,
#             'registration_no': 'GHI789',
#             'rego_state': 'VIC',
#             'vin': 'WBA3A5C50EF123456',
#             'make': 'BMW',
#             'model': 'X3',
#             'sub_model': 'xDrive30i',
#             'year': 2021,
#             'body_type': 'SUV',
#             'fuel_type': 'Petrol',
#             'transmission': 'Automatic',
#             'color': 'Blue',
#             'odometer_reading': 15000,
#             'notes': ''
#         },
#         {
#             'customer_id': customers[1].id,
#             'registration_no': 'JKL012',
#             'rego_state': 'VIC',
#             'vin': 'SAJAA51D9EG123456',
#             'make': 'Jaguar',
#             'model': 'F-Pace',
#             'sub_model': 'R-Sport',
#             'year': 2020,
#             'body_type': 'SUV',
#             'fuel_type': 'Diesel',
#             'transmission': 'Automatic',
#             'color': 'Red',
#             'odometer_reading': 28000,
#             'notes': 'Under warranty'
#         },
#         # Customer 3: Michael Brown (index 2) - 1 vehicle
#         {
#             'customer_id': customers[2].id,
#             'registration_no': 'MNO345',
#             'rego_state': 'QLD',
#             'vin': 'JF1GP7LC5DH123456',
#             'make': 'Subaru',
#             'model': 'Outback',
#             'sub_model': 'Premium',
#             'year': 2017,
#             'body_type': 'Wagon',
#             'fuel_type': 'Petrol',
#             'transmission': 'CVT',
#             'color': 'Green',
#             'odometer_reading': 95000,
#             'notes': 'AWD service needed'
#         },
#         # Customer 4: Emily Davis (index 3) - 1 vehicle
#         {
#             'customer_id': customers[3].id,
#             'registration_no': 'PQR678',
#             'rego_state': 'WA',
#             'vin': 'JM0KE107200123456',
#             'make': 'Mazda',
#             'model': 'CX-5',
#             'sub_model': 'Touring',
#             'year': 2022,
#             'body_type': 'SUV',
#             'fuel_type': 'Petrol',
#             'transmission': 'Automatic',
#             'color': 'Titanium',
#             'odometer_reading': 8000,
#             'notes': 'New vehicle'
#         },
#         # Customer 5: David Wilson (index 4) - 2 vehicles
#         {
#             'customer_id': customers[4].id,
#             'registration_no': 'STU901',
#             'rego_state': 'SA',
#             'vin': 'KL8CD6SA9GC123456',
#             'make': 'Hyundai',
#             'model': 'Tucson',
#             'sub_model': 'Highlander',
#             'year': 2019,
#             'body_type': 'SUV',
#             'fuel_type': 'Diesel',
#             'transmission': 'Automatic',
#             'color': 'Grey',
#             'odometer_reading': 55000,
#             'notes': ''
#         },
#         {
#             'customer_id': customers[4].id,
#             'registration_no': 'VWX234',
#             'rego_state': 'SA',
#             'vin': 'WVWZZZ1KZAW123456',
#             'make': 'Volkswagen',
#             'model': 'Golf',
#             'sub_model': 'Comfortline',
#             'year': 2016,
#             'body_type': 'Hatchback',
#             'fuel_type': 'Petrol',
#             'transmission': 'DSG',
#             'color': 'White',
#             'odometer_reading': 112000,
#             'notes': 'Needs major service'
#         },
#         # Customer 6: Taylor Transport (index 5) - 3 vehicles
#         {
#             'customer_id': customers[5].id,
#             'registration_no': '1ABC123',
#             'rego_state': 'NSW',
#             'vin': 'YV1MW445462123456',
#             'make': 'Volvo',
#             'model': 'FH',
#             'year': 2020,
#             'body_type': 'Truck',
#             'fuel_type': 'Diesel',
#             'transmission': 'Manual',
#             'color': 'White',
#             'odometer_reading': 150000,
#             'notes': 'Fleet vehicle #1'
#         },
#         {
#             'customer_id': customers[5].id,
#             'registration_no': '2ABC123',
#             'rego_state': 'NSW',
#             'vin': 'YV1MW445462123457',
#             'make': 'Volvo',
#             'model': 'FH',
#             'year': 2020,
#             'body_type': 'Truck',
#             'fuel_type': 'Diesel',
#             'transmission': 'Manual',
#             'color': 'White',
#             'odometer_reading': 135000,
#             'notes': 'Fleet vehicle #2'
#         },
#         {
#             'customer_id': customers[5].id,
#             'registration_no': '3ABC123',
#             'rego_state': 'NSW',
#             'vin': 'YV1MW445462123458',
#             'make': 'Scania',
#             'model': 'R-Series',
#             'year': 2021,
#             'body_type': 'Truck',
#             'fuel_type': 'Diesel',
#             'transmission': 'Automated',
#             'color': 'Silver',
#             'odometer_reading': 98000,
#             'notes': 'Fleet vehicle #3'
#         },
#         # Customer 7: Martinez Auto Group (index 6) - 2 vehicles
#         {
#             'customer_id': customers[6].id,
#             'registration_no': 'MRT001',
#             'rego_state': 'VIC',
#             'vin': 'WMWMF72040T123456',
#             'make': 'Mini',
#             'model': 'Cooper S',
#             'year': 2023,
#             'body_type': 'Hatchback',
#             'fuel_type': 'Petrol',
#             'transmission': 'Manual',
#             'color': 'British Racing Green',
#             'odometer_reading': 1500,
#             'notes': 'Demo vehicle'
#         },
#         {
#             'customer_id': customers[6].id,
#             'registration_no': 'MRT002',
#             'rego_state': 'VIC',
#             'vin': 'WP0ZZZ99ZGS123456',
#             'make': 'Porsche',
#             'model': 'Macan',
#             'sub_model': 'S',
#             'year': 2022,
#             'body_type': 'SUV',
#             'fuel_type': 'Petrol',
#             'transmission': 'PDK',
#             'color': 'Carrera White',
#             'odometer_reading': 5200,
#             'notes': 'Showroom vehicle'
#         },
#         # Customer 8: Anderson Fleet Services (index 7) - 2 vehicles
#         {
#             'customer_id': customers[7].id,
#             'registration_no': 'AFS001',
#             'rego_state': 'QLD',
#             'vin': '1FT7W2BT5KE123456',
#             'make': 'Ford',
#             'model': 'Ranger',
#             'sub_model': 'Wildtrak',
#             'year': 2021,
#             'body_type': 'Ute',
#             'fuel_type': 'Diesel',
#             'transmission': 'Automatic',
#             'color': 'Blue',
#             'odometer_reading': 42000,
#             'notes': 'Fleet vehicle'
#         },
#         {
#             'customer_id': customers[7].id,
#             'registration_no': 'AFS002',
#             'rego_state': 'QLD',
#             'vin': 'MNAUMFF50HW123456',
#             'make': 'Mitsubishi',
#             'model': 'Triton',
#             'sub_model': 'GLX+',
#             'year': 2020,
#             'body_type': 'Ute',
#             'fuel_type': 'Diesel',
#             'transmission': 'Manual',
#             'color': 'Silver',
#             'odometer_reading': 65000,
#             'notes': 'Fleet vehicle'
#         },
#     ]
    
#     vehicles = []
#     for data in vehicle_definitions:
#         vehicle = Vehicle(**data)
#         db.session.add(vehicle)
#         vehicles.append(vehicle)
    
#     db.session.commit()
#     print(f"Created {len(vehicles)} vehicles")
    
#     print("Creating leads...")
#     leads = []
#     lead_data = [
#         {
#             'full_name': 'Alex Thompson',
#             'email': 'alex.thompson@email.com',
#             'phone': '0490123456',
#             'rego': 'NEW001',
#             'rego_state': 'NSW',
#             'vehicle_description': '2023 Toyota Camry',
#             'address': '123 New Street, Sydney NSW 2000',
#             'notes': 'Interested in service booking',
#             'converted': False,
#         },
#         {
#             'full_name': 'Lisa Wang',
#             'email': 'lisa.w@outlook.com',
#             'phone': '0491234567',
#             'rego': 'NEW002',
#             'rego_state': 'VIC',
#             'vehicle_description': '2019 Mazda CX-9',
#             'address': '456 New Avenue, Melbourne VIC 3000',
#             'notes': 'Calls after 5pm',
#             'converted': False,
#         },
#         {
#             'full_name': 'Daniel Kim',
#             'email': 'daniel.k@yahoo.com',
#             'phone': '0492345678',
#             'rego': 'NEW003',
#             'rego_state': 'QLD',
#             'vehicle_description': '2020 Ford Everest',
#             'address': '789 New Road, Brisbane QLD 4000',
#             'notes': 'Needs urgent service',
#             'converted': False,
#         },
#         {
#             'full_name': 'Rachel Green',
#             'email': 'rachel.green@gmail.com',
#             'phone': '0493456789',
#             'rego': 'CONV001',
#             'rego_state': 'NSW',
#             'vehicle_description': '2021 Honda CR-V',
#             'address': '321 Converted St, Sydney NSW 2000',
#             'notes': 'Converted to booking',
#             'converted': True,
#         },
#         {
#             'full_name': 'Tom Harris',
#             'email': 'tom.h@hotmail.com',
#             'phone': '0494567890',
#             'rego': 'CONV002',
#             'rego_state': 'VIC',
#             'vehicle_description': '2022 Subaru Forester',
#             'address': '654 Converted Ave, Melbourne VIC 3000',
#             'notes': 'Converted lead - follow up',
#             'converted': True,
#         },
#         {
#             'full_name': 'Emma Watson',
#             'email': 'emma.w@email.com',
#             'phone': '0495678901',
#             'rego': 'NEW004',
#             'rego_state': 'WA',
#             'vehicle_description': '2018 Hyundai Santa Fe',
#             'address': '987 New Lane, Perth WA 6000',
#             'notes': 'Inquiry about fleet discount',
#             'converted': False,
#         },
#     ]
    
#     for data in lead_data:
#         lead = Lead(**data)
#         db.session.add(lead)
#         leads.append(lead)
    
#     db.session.commit()
#     print(f"Created {len(leads)} leads")
    
#     print("Creating bookings...")
#     bookings = []
    
#     now = utc_now()
#     today = utc_today()
    
#     # Helper function to create time
#     def make_time(hour, minute):
#         return now.replace(hour=hour, minute=minute, second=0, microsecond=0).time()
    
#     # Base booking data
#     booking_base = [
#         # Booking 1: John Smith's Honda Civic
#         {
#             'customer_id': customers[0].id,
#             'vehicle_id': vehicles[0].id,
#             'customer_name': 'John Smith',
#             'customer_email': 'john.smith@gmail.com',
#             'customer_phone': '0412345678',
#             'customer_address': '123 Main St, Sydney NSW 2000',
#             'vehicle_rego': 'ABC123',
#             'vehicle_rego_state': 'NSW',
#             'vehicle_vin': '1HGCM82633A123456',
#             'vehicle_make': 'Honda',
#             'vehicle_model': 'Civic',
#             'vehicle_year': 2020,
#             'service_type': 'engine_scan',
#             'service_description': 'Full diagnostic scan and engine check',
#             'customer_notes': 'Check engine light on dashboard',
#             'special_instructions': 'Call 30 mins before arrival',
#             'preferred_date': today + timedelta(days=3),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today + timedelta(days=5),
#             'scheduled_time': make_time(9, 0),
#             'duration_minutes': 90,
#             'status': 'confirmed',
#             'priority': 'high',
#             'service_address': '123 Main St, Sydney NSW 2000',
#         },
#         # Booking 2: Sarah Johnson's Mercedes-Benz
#         {
#             'customer_id': customers[1].id,
#             'vehicle_id': vehicles[2].id,
#             'customer_name': 'Sarah Johnson',
#             'customer_email': 'sarah.j@outlook.com',
#             'customer_phone': '0423456789',
#             'customer_address': '456 Beach Rd, Melbourne VIC 3000',
#             'vehicle_rego': 'DEF456',
#             'vehicle_rego_state': 'VIC',
#             'vehicle_vin': 'WDDGF4HB7CG123456',
#             'vehicle_make': 'Mercedes-Benz',
#             'vehicle_model': 'C200',
#             'vehicle_year': 2019,
#             'service_type': 'brake_inspection',
#             'service_description': 'Complete brake system inspection and service',
#             'customer_notes': 'Squeaking noise when braking',
#             'special_instructions': 'Use genuine Mercedes parts only',
#             'preferred_date': today + timedelta(days=1),
#             'preferred_time_slot': 'afternoon',
#             'scheduled_date': today + timedelta(days=2),
#             'scheduled_time': make_time(14, 0),
#             'duration_minutes': 60,
#             'status': 'pending',
#             'priority': 'normal',
#             'service_address': '456 Beach Rd, Melbourne VIC 3000',
#         },
#         # Booking 3: Michael Brown's Subaru Outback
#         {
#             'customer_id': customers[2].id,
#             'vehicle_id': vehicles[4].id,
#             'customer_name': 'Michael Brown',
#             'customer_email': 'michael.brown@hotmail.com',
#             'customer_phone': '0434567890',
#             'customer_address': '789 Park Ave, Brisbane QLD 4000',
#             'vehicle_rego': 'MNO345',
#             'vehicle_rego_state': 'QLD',
#             'vehicle_vin': 'JF1GP7LC5DH123456',
#             'vehicle_make': 'Subaru',
#             'vehicle_model': 'Outback',
#             'vehicle_year': 2017,
#             'service_type': 'wheel_alignment',
#             'service_description': 'Wheel alignment and balancing',
#             'customer_notes': 'Steering pulls to the left',
#             'special_instructions': '',
#             'preferred_date': today + timedelta(days=7),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today + timedelta(days=8),
#             'scheduled_time': make_time(10, 0),
#             'duration_minutes': 45,
#             'status': 'pending',
#             'priority': 'normal',
#             'service_address': '789 Park Ave, Brisbane QLD 4000',
#         },
#         # Booking 4: Taylor Transport - Volvo FH Truck
#         {
#             'customer_id': customers[5].id,
#             'vehicle_id': vehicles[7].id,
#             'customer_name': 'Robert Taylor (Taylor Transport)',
#             'customer_email': 'robert.taylor@taylortransport.com.au',
#             'customer_phone': '0467890123',
#             'customer_address': '987 Industrial Dr, Sydney NSW 2145',
#             'vehicle_rego': '1ABC123',
#             'vehicle_rego_state': 'NSW',
#             'vehicle_vin': 'YV1MW445462123456',
#             'vehicle_make': 'Volvo',
#             'vehicle_model': 'FH',
#             'vehicle_year': 2020,
#             'service_type': 'engine_scan',
#             'service_description': 'Full heavy vehicle diagnostic',
#             'customer_notes': 'Check engine power loss on hills',
#             'special_instructions': 'Fleet priority - needs urgent completion',
#             'preferred_date': today + timedelta(days=2),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today + timedelta(days=3),
#             'scheduled_time': make_time(8, 30),
#             'duration_minutes': 120,
#             'status': 'confirmed',
#             'priority': 'urgent',
#             'service_address': '987 Industrial Dr, Sydney NSW 2145',
#         },
#         # Booking 5: Converted Lead - Rachel Green
#         {
#             'customer_name': 'Rachel Green',
#             'customer_email': 'rachel.green@gmail.com',
#             'customer_phone': '0493456789',
#             'customer_address': '321 Converted St, Sydney NSW 2000',
#             'vehicle_rego': 'CONV001',
#             'vehicle_rego_state': 'NSW',
#             'vehicle_make': 'Honda',
#             'vehicle_model': 'CR-V',
#             'vehicle_year': 2021,
#             'service_type': 'minor_service',
#             'service_description': 'Routine minor service (oil and filters)',
#             'customer_notes': 'Converted from lead',
#             'special_instructions': '',
#             'preferred_date': today + timedelta(days=10),
#             'preferred_time_slot': 'afternoon',
#             'scheduled_date': today + timedelta(days=12),
#             'scheduled_time': make_time(13, 0),
#             'duration_minutes': 60,
#             'status': 'pending',
#             'priority': 'normal',
#             'service_address': '321 Converted St, Sydney NSW 2000',
#         },
#         # Booking 6: Martinez Auto Group - Porsche Macan
#         {
#             'customer_id': customers[6].id,
#             'vehicle_id': vehicles[10].id,
#             'customer_name': 'Jennifer Martinez (Martinez Auto Group)',
#             'customer_email': 'jen@martinezautogroup.com.au',
#             'customer_phone': '0478901234',
#             'customer_address': '234 Showroom Blvd, Melbourne VIC 3150',
#             'vehicle_rego': 'MRT002',
#             'vehicle_rego_state': 'VIC',
#             'vehicle_vin': 'WP0ZZZ99ZGS123456',
#             'vehicle_make': 'Porsche',
#             'vehicle_model': 'Macan',
#             'vehicle_year': 2022,
#             'service_type': 'major_service',
#             'service_description': 'Major service and inspection',
#             'customer_notes': 'Pre-delivery inspection required',
#             'special_instructions': 'Must be completed by Friday for delivery',
#             'preferred_date': today + timedelta(days=4),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today + timedelta(days=4),
#             'scheduled_time': make_time(9, 30),
#             'duration_minutes': 180,
#             'status': 'in_progress',
#             'priority': 'high',
#             'service_address': '234 Showroom Blvd, Melbourne VIC 3150',
#         },
#         # Booking 7: Anderson Fleet Services - Ford Ranger
#         {
#             'customer_id': customers[7].id,
#             'vehicle_id': vehicles[11].id,
#             'customer_name': 'James Anderson (Anderson Fleet Services)',
#             'customer_email': 'james.anderson@afs.com.au',
#             'customer_phone': '0489012345',
#             'customer_address': '567 Logistics Way, Brisbane QLD 4008',
#             'vehicle_rego': 'AFS001',
#             'vehicle_rego_state': 'QLD',
#             'vehicle_vin': '1FT7W2BT5KE123456',
#             'vehicle_make': 'Ford',
#             'vehicle_model': 'Ranger',
#             'vehicle_year': 2021,
#             'service_type': 'tyre_replacement',
#             'service_description': 'Replace all 4 tyres and wheel alignment',
#             'customer_notes': 'Fleet vehicle - high mileage',
#             'special_instructions': 'Use all-terrain tyres',
#             'preferred_date': today + timedelta(days=5),
#             'preferred_time_slot': 'afternoon',
#             'scheduled_date': today + timedelta(days=6),
#             'scheduled_time': make_time(15, 0),
#             'duration_minutes': 90,
#             'status': 'confirmed',
#             'priority': 'normal',
#             'service_address': '567 Logistics Way, Brisbane QLD 4008',
#         },
#         # Booking 8: David Wilson - Hyundai Tucson
#         {
#             'customer_id': customers[4].id,
#             'vehicle_id': vehicles[5].id,
#             'customer_name': 'David Wilson',
#             'customer_email': 'david.wilson@yahoo.com',
#             'customer_phone': '0456789012',
#             'customer_address': '654 Valley Rd, Adelaide SA 5000',
#             'vehicle_rego': 'STU901',
#             'vehicle_rego_state': 'SA',
#             'vehicle_vin': 'KL8CD6SA9GC123456',
#             'vehicle_make': 'Hyundai',
#             'vehicle_model': 'Tucson',
#             'vehicle_year': 2019,
#             'service_type': 'air_con_service',
#             'service_description': 'Air conditioning service and regas',
#             'customer_notes': 'Aircon not cooling properly',
#             'special_instructions': 'Check for leaks',
#             'preferred_date': today + timedelta(days=6),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today + timedelta(days=7),
#             'scheduled_time': make_time(11, 0),
#             'duration_minutes': 60,
#             'status': 'pending',
#             'priority': 'normal',
#             'service_address': '654 Valley Rd, Adelaide SA 5000',
#         },
#         # Booking 9: Completed booking - Emily Davis
#         {
#             'customer_id': customers[3].id,
#             'vehicle_id': vehicles[4].id,
#             'customer_name': 'Emily Davis',
#             'customer_email': 'emily.davis@gmail.com',
#             'customer_phone': '0445678901',
#             'customer_address': '321 Hill St, Perth WA 6000',
#             'vehicle_rego': 'PQR678',
#             'vehicle_rego_state': 'WA',
#             'vehicle_vin': 'JM0KE107200123456',
#             'vehicle_make': 'Mazda',
#             'vehicle_model': 'CX-5',
#             'vehicle_year': 2022,
#             'service_type': 'first_service',
#             'service_description': 'First 1000km inspection and service',
#             'customer_notes': 'New vehicle - first service',
#             'special_instructions': '',
#             'preferred_date': today - timedelta(days=5),
#             'preferred_time_slot': 'morning',
#             'scheduled_date': today - timedelta(days=3),
#             'scheduled_time': (now - timedelta(days=3)).replace(hour=10, minute=0, second=0, microsecond=0).time(),
#             'duration_minutes': 60,
#             'status': 'completed',
#             'priority': 'normal',
#             'service_address': '321 Hill St, Perth WA 6000',
#         },
#         # Booking 10: Cancelled booking
#         {
#             'customer_id': customers[1].id,
#             'vehicle_id': vehicles[3].id,
#             'customer_name': 'Sarah Johnson',
#             'customer_email': 'sarah.j@outlook.com',
#             'customer_phone': '0423456789',
#             'customer_address': '456 Beach Rd, Melbourne VIC 3000',
#             'vehicle_rego': 'JKL012',
#             'vehicle_rego_state': 'VIC',
#             'vehicle_vin': 'SAJAA51D9EG123456',
#             'vehicle_make': 'Jaguar',
#             'vehicle_model': 'F-Pace',
#             'vehicle_year': 2020,
#             'service_type': 'diagnostic',
#             'service_description': 'Full diagnostic check',
#             'customer_notes': 'Engine warning light',
#             'special_instructions': '',
#             'preferred_date': today + timedelta(days=1),
#             'preferred_time_slot': 'afternoon',
#             'scheduled_date': today + timedelta(days=1),
#             'scheduled_time': (now + timedelta(days=1)).replace(hour=14, minute=30, second=0, microsecond=0).time(),
#             'duration_minutes': 60,
#             'status': 'cancelled',
#             'priority': 'normal',
#             'service_address': '456 Beach Rd, Melbourne VIC 3000',
#         },
#     ]
    
#     for data in booking_base:
#         booking = Booking(**data)
#         db.session.add(booking)
#         bookings.append(booking)
    
#     db.session.commit()
#     print(f"Created {len(bookings)} bookings")
    
#     # Link converted leads to bookings
#     print("Linking converted leads to bookings...")
#     converted_leads = Lead.query.filter_by(converted=True).all()
    
#     # Converted lead 1: Rachel Green -> Booking 5
#     if len(converted_leads) >= 2 and len(bookings) >= 5:
#         converted_leads[0].booking_id = bookings[4].id
#         converted_leads[0].converted_at = utc_now()
#         db.session.commit()
#         print(f"Linked lead '{converted_leads[0].full_name}' to booking {bookings[4].booking_number}")
    
#     print("Linking complete!")
#     print(f"\nSummary:")
#     print(f"- Customers: {Customer.query.count()}")
#     print(f"- Vehicles: {Vehicle.query.count()}")
#     print(f"- Leads: {Lead.query.count()}")
#     print(f"- Bookings: {Booking.query.count()}")
    
#     # Update booking numbers for all bookings
#     print("\nUpdating booking numbers...")
#     for booking in Booking.query.all():
#         if not booking.booking_number:
#             booking.booking_number = booking.generate_booking_number()
#     db.session.commit()
    
#     print("Seeding complete!")

# if __name__ == "__main__":
#     # Import app and create context if needed
#     # If you have a create_app function:
#     from app import create_app
#     app = create_app()
#     with app.app_context():
#         seed_database()


# seeds/bookings_seed.py

from datetime import datetime, timedelta
from extensions import db
from models import Booking, Customer, Vehicle
import random

def generate_booking_number():
    """Generate a unique booking number"""
    now = datetime.now()
    date_part = now.strftime('%Y%m%d')
    
    # Get the count of bookings created today
    today_start = datetime(now.year, now.month, now.day, 0, 0, 0)
    today_count = Booking.query.filter(Booking.created_at >= today_start).count()
    
    return f"BK-{date_part}-{str(today_count + 1).zfill(4)}"

def seed_bookings():
    """Create seed bookings with multiple bookings on the same day"""
    
    # First, ensure we have customers and vehicles
    customers = Customer.query.all()
    vehicles = Vehicle.query.all()
    
    if not customers or not vehicles:
        print("Please seed customers and vehicles first")
        return
    
    # Base date for bookings (next week's Monday)
    base_date = datetime.now().date() + timedelta(days=7 - datetime.now().weekday())
    
    # Service types
    service_types = [
        'engine_scan', 'diagnostic_test', 'oil_change', 'brake_service', 
        'transmission_service', 'battery_test', 'wheel_alignment', 'aircon_service',
        'major_service', 'minor_service', 'engine_repair', 'electrical_diagnostic'
    ]
    
    # Statuses with weights (more pending and confirmed)
    statuses = ['pending', 'pending', 'confirmed', 'confirmed', 'confirmed', 
                'in_progress', 'completed', 'completed', 'cancelled', 'no_show']
    
    # Priorities
    priorities = ['low', 'normal', 'normal', 'high', 'urgent']
    
    # Time slots
    time_slots = [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', 
        '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ]
    
    # Create bookings for each day of the week
    for day_offset in range(0, 7):  # One week
        current_date = base_date + timedelta(days=day_offset)
        
        # Number of bookings per day (5-10)
        num_bookings = random.randint(5, 10)
        
        # Shuffle customers and vehicles for variety
        shuffled_customers = random.sample(customers, min(len(customers), num_bookings))
        shuffled_vehicles = random.sample(vehicles, min(len(vehicles), num_bookings))
        
        # Create bookings for this day
        for i in range(num_bookings):
            # Pick customer and vehicle
            customer = shuffled_customers[i % len(shuffled_customers)]
            vehicle = shuffled_vehicles[i % len(shuffled_vehicles)]
            
            # Random time slot (spread throughout the day)
            time_str = random.choice(time_slots)
            scheduled_time = datetime.strptime(time_str, '%H:%M').time()
            
            # Random status
            status = random.choice(statuses)
            priority = random.choice(priorities)
            service_type = random.choice(service_types)
            
            # Generate unique booking number
            booking_number = generate_booking_number()
            
            # Create booking
            booking = Booking(
                booking_number=booking_number,
                customer_id=customer.id,
                vehicle_id=vehicle.id,
                customer_name=f"{customer.first_name} {customer.last_name}",
                customer_email=customer.email,
                customer_phone=customer.phone,
                customer_address=customer.address,
                vehicle_rego=vehicle.registration_no,
                vehicle_rego_state=vehicle.rego_state,
                vehicle_make=vehicle.make,
                vehicle_model=vehicle.model,
                vehicle_year=vehicle.year,
                service_type=service_type,
                service_description=f"Standard {service_type.replace('_', ' ')} service",
                customer_notes=f"Customer requested {service_type.replace('_', ' ')}",
                scheduled_date=current_date,
                scheduled_time=scheduled_time,
                status=status,
                priority=priority,
                duration_minutes=random.choice([30, 45, 60, 90, 120])
            )
            
            # Set timestamps based on status
            if status == 'confirmed':
                booking.confirmed_at = datetime.now()
            elif status == 'in_progress':
                booking.confirmed_at = datetime.now() - timedelta(hours=2)
            elif status == 'completed':
                booking.confirmed_at = datetime.now() - timedelta(hours=4)
                booking.completed_at = datetime.now() - timedelta(hours=1)
            elif status == 'cancelled':
                booking.cancelled_at = datetime.now() - timedelta(hours=1)
            
            db.session.add(booking)
            
            # Commit in batches to avoid transaction issues
            if (i + 1) % 10 == 0:
                db.session.commit()
                print(f"✅ Committed {i + 1} bookings")
    
    # Final commit
    db.session.commit()
    print(f"✅ Created {Booking.query.count()} bookings with multiple bookings per day")


def seed_specific_day_bookings():
    """Create multiple bookings specifically for today and tomorrow"""
    
    customers = Customer.query.all()
    vehicles = Vehicle.query.all()
    
    if not customers or not vehicles:
        print("Please seed customers and vehicles first")
        return
    
    # Today's date
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    # Create 15 bookings for today
    print(f"Creating 15 bookings for today ({today})")
    create_day_bookings(today, customers, vehicles, 15)
    
    # Create 12 bookings for tomorrow
    print(f"Creating 12 bookings for tomorrow ({tomorrow})")
    create_day_bookings(tomorrow, customers, vehicles, 12)
    
    db.session.commit()
    print(f"✅ Created bookings for today and tomorrow")


def create_day_bookings(date, customers, vehicles, count):
    """Helper to create multiple bookings for a specific day"""
    
    service_types = [
        'engine_scan', 'diagnostic_test', 'oil_change', 'brake_service', 
        'transmission_service', 'battery_test', 'wheel_alignment', 'aircon_service',
        'major_service', 'minor_service', 'engine_repair', 'electrical_diagnostic'
    ]
    
    statuses = ['pending', 'confirmed', 'in_progress', 'completed']
    priorities = ['low', 'normal', 'high']
    
    # Time slots with 30-minute intervals
    time_slots = [
        '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', 
        '11:00', '11:30', '12:00', '12:30', '13:00', '13:30',
        '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
    ]
    
    # Shuffle for variety
    shuffled_customers = random.sample(customers, min(len(customers), count))
    shuffled_vehicles = random.sample(vehicles, min(len(vehicles), count))
    
    for i in range(count):
        customer = shuffled_customers[i % len(shuffled_customers)]
        vehicle = shuffled_vehicles[i % len(shuffled_vehicles)]
        
        time_str = time_slots[i % len(time_slots)]
        scheduled_time = datetime.strptime(time_str, '%H:%M').time()
        
        # Make some bookings have same status for easier testing
        if i < 5:
            status = 'pending'
        elif i < 10:
            status = 'confirmed'
        elif i < 13:
            status = 'in_progress'
        else:
            status = 'completed'
        
        priority = priorities[i % len(priorities)]
        service_type = random.choice(service_types)
        
        # Generate unique booking number
        booking_number = generate_booking_number()
        
        booking = Booking(
            booking_number=booking_number,
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            customer_name=f"{customer.first_name} {customer.last_name}",
            customer_email=customer.email,
            customer_phone=customer.phone,
            customer_address=customer.address,
            vehicle_rego=vehicle.registration_no,
            vehicle_rego_state=vehicle.rego_state,
            vehicle_make=vehicle.make,
            vehicle_model=vehicle.model,
            vehicle_year=vehicle.year,
            service_type=service_type,
            service_description=f"Standard {service_type.replace('_', ' ')} service",
            customer_notes=f"Customer requested {service_type.replace('_', ' ')} - Booking #{i+1}",
            scheduled_date=date,
            scheduled_time=scheduled_time,
            status=status,
            priority=priority,
            duration_minutes=random.choice([30, 45, 60, 90])
        )
        
        # Set timestamps based on status
        if status == 'confirmed':
            booking.confirmed_at = datetime.now()
        elif status == 'in_progress':
            booking.confirmed_at = datetime.now() - timedelta(hours=1)
        elif status == 'completed':
            booking.confirmed_at = datetime.now() - timedelta(hours=3)
            booking.completed_at = datetime.now() - timedelta(hours=1)
        
        db.session.add(booking)


def seed_booking_with_customer_and_vehicle():
    """Seed a complete booking with customer and vehicle data"""
    
    # Create a test customer if not exists
    customer = Customer.query.filter_by(email='test@example.com').first()
    if not customer:
        customer = Customer(
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            phone='0400 123 456',
            mobile='0400 123 456',
            address='123 Main Street',
            city='Sydney',
            state='NSW',
            postal_code='2000',
            country='Australia',
            active=True
        )
        db.session.add(customer)
        db.session.commit()
        print(f"✅ Created customer: {customer.full_name}")
    
    # Create a test vehicle
    vehicle = Vehicle.query.filter_by(registration_no='ABC123').first()
    if not vehicle:
        vehicle = Vehicle(
            customer_id=customer.id,
            registration_no='ABC123',
            rego_state='NSW',
            make='Toyota',
            model='Camry',
            year=2020,
            color='Silver',
            vin='JTDBF123456789012',
            active=True
        )
        db.session.add(vehicle)
        db.session.commit()
        print(f"✅ Created vehicle: {vehicle.registration_no}")
    
    # Create multiple bookings for this customer/vehicle
    service_types = ['engine_scan', 'oil_change', 'brake_service', 'major_service']
    statuses = ['pending', 'confirmed', 'completed', 'cancelled']
    
    for i in range(5):
        date = datetime.now().date() + timedelta(days=i)
        status = statuses[i % len(statuses)]
        
        booking = Booking(
            booking_number=generate_booking_number(),
            customer_id=customer.id,
            vehicle_id=vehicle.id,
            customer_name=customer.full_name,
            customer_email=customer.email,
            customer_phone=customer.phone,
            customer_address=customer.address,
            vehicle_rego=vehicle.registration_no,
            vehicle_rego_state=vehicle.rego_state,
            vehicle_make=vehicle.make,
            vehicle_model=vehicle.model,
            vehicle_year=vehicle.year,
            service_type=random.choice(service_types),
            service_description=f"Service booking #{i+1}",
            customer_notes=f"Regular service booking - #{i+1}",
            scheduled_date=date,
            scheduled_time=datetime.strptime('09:00', '%H:%M').time(),
            status=status,
            priority='normal',
            duration_minutes=60
        )
        
        if status == 'confirmed':
            booking.confirmed_at = datetime.now()
        elif status == 'completed':
            booking.confirmed_at = datetime.now() - timedelta(days=1)
            booking.completed_at = datetime.now()
        
        db.session.add(booking)
    
    db.session.commit()
    print(f"✅ Created 5 bookings for {customer.full_name}")


def clear_bookings():
    """Clear all bookings (useful for testing)"""
    try:
        num_deleted = Booking.query.delete()
        db.session.commit()
        print(f"✅ Deleted {num_deleted} bookings")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error clearing bookings: {e}")


# Run the seeds
if __name__ == '__main__':
    import sys
    sys.path.append('.')
    
    from app import create_app
    app = create_app()
    
    with app.app_context():
        print("🌱 Seeding bookings...")
        
        # Option: Clear existing bookings first (uncomment if needed)
        # clear_bookings()
        
        # Option 1: Create random bookings across a week
        seed_bookings()
        
        # Option 2: Create specific bookings for today and tomorrow
        seed_specific_day_bookings()
        
        # Option 3: Create bookings for a specific customer
        seed_booking_with_customer_and_vehicle()
        
        print("✨ Seeding complete!")