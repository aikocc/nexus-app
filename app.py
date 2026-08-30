from flask import Flask, render_template
from dotenv import load_dotenv
import os
from extensions import db, csrf
from models import Customer, Vehicle, Leads
from routes import register_blueprints
import logging


load_dotenv()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///workshop.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    csrf.init_app(app)
    
    register_blueprints(app)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.context_processor
    def utility_processor():
        return {
            'get_customer_full_name': lambda customer: customer.full_name if customer else ''
        }
    
    with app.app_context():
        db.create_all()
        if Customer.query.count() == 0:
            seed_data()
    
    return app


def seed_data():
    # ========== CUSTOMERS ==========
    customer1 = Customer(
        first_name='John',
        last_name='Smith',
        company_name=None,
        email='john.smith@email.com',
        phone='555-1234',
        mobile='555-5678',
        address='123 Main Street',
        city='Springfield',
        state='IL',
        postal_code='62701',
        country='USA',
        tax_id='123-45-6789',
        is_company=False,
        notes='Prefers email contact. Long-time customer.',
        active=True
    )
    
    customer2 = Customer(
        first_name='Maria',
        last_name='Garcia',
        company_name='Garcia Logistics',
        email='maria@garcialogistics.com',
        phone='555-8765',
        mobile='555-4321',
        address='456 Industrial Blvd',
        city='Denver',
        state='CO',
        postal_code='80202',
        country='USA',
        tax_id='98-765-4321',
        is_company=True,
        notes='Fleet customer. Needs priority service.',
        active=True
    )
    
    customer3 = Customer(
        first_name='Robert',
        last_name='Chen',
        company_name=None,
        email='robert.chen@outlook.com',
        phone='555-9988',
        mobile='555-7766',
        address='789 Oak Avenue',
        city='Los Angeles',
        state='CA',
        postal_code='90001',
        country='USA',
        tax_id=None,
        is_company=False,
        notes='Interested in electric vehicles.',
        active=True
    )
    
    customer4 = Customer(
        first_name='Sarah',
        last_name='Williams',
        company_name='Williams & Sons Auto Repair',
        email='sarah@williamsauto.com',
        phone='555-4455',
        mobile='555-6677',
        address='321 Garage Lane',
        city='Houston',
        state='TX',
        postal_code='77001',
        country='USA',
        tax_id='45-678-9012',
        is_company=True,
        notes='Trade partner. Offers mechanic services.',
        active=True
    )
    
    db.session.add_all([customer1, customer2, customer3, customer4])
    db.session.commit()
    
    # ========== VEHICLES ==========
    vehicle1 = Vehicle(
        customer_id=customer1.id,
        registration_no='ABC-123',
        rego_state='IL',
        vin='1HGCM82633A123456',
        make='Toyota',
        model='Corolla',
        sub_model='LE',
        series='E210',
        year=2020,
        body_type='Sedan',
        drive_type='FWD',
        fuel_type='Petrol',
        transmission='Automatic',
        engine_spec='1.8L 4-cylinder 139 hp',
        doors=4,
        chassis_no='TMC2020A12345',
        color='Silver',
        odometer_reading=45000,
        notes='Regular maintenance up to date.',
        active=True
    )
    
    vehicle2 = Vehicle(
        customer_id=customer2.id,
        registration_no='XYZ-789',
        rego_state='CO',
        vin='5J6RM4H79LL123456',
        make='Honda',
        model='CR-V',
        sub_model='EX-L',
        series='RW',
        year=2019,
        body_type='SUV',
        drive_type='AWD',
        fuel_type='Petrol',
        transmission='CVT',
        engine_spec='1.5L Turbo 4-cylinder 190 hp',
        doors=4,
        chassis_no='HMC2019B67890',
        color='Blue',
        odometer_reading=68000,
        notes='Company vehicle. Fleet maintenance schedule.',
        active=True
    )
    
    vehicle3 = Vehicle(
        customer_id=customer3.id,
        registration_no='EV-2023',
        rego_state='CA',
        vin='1N4AZ1CP0JC123456',
        make='Tesla',
        model='Model 3',
        sub_model='Long Range',
        series='Performance',
        year=2023,
        body_type='Sedan',
        drive_type='AWD',
        fuel_type='Electric',
        transmission='Single Speed',
        engine_spec='Dual Motor - 450 hp',
        doors=4,
        chassis_no='TSLA2023C98765',
        color='White',
        odometer_reading=12000,
        notes='Charging installed at home.',
        active=True
    )
    
    vehicle4 = Vehicle(
        customer_id=customer1.id,
        registration_no='TRUCK-456',
        rego_state='IL',
        vin='1FT7X2BT3KE123456',
        make='Ford',
        model='F-150',
        sub_model='Lariat',
        series='SuperCrew',
        year=2021,
        body_type='Pickup Truck',
        drive_type='4WD',
        fuel_type='Diesel',
        transmission='Automatic',
        engine_spec='3.0L Power Stroke V6 250 hp',
        doors=4,
        chassis_no='FORD2021D54321',
        color='Black',
        odometer_reading=32000,
        notes='Used for towing. Has tow package.',
        active=True
    )
    
    vehicle5 = Vehicle(
        customer_id=customer2.id,
        registration_no='VAN-2022',
        rego_state='CO',
        vin='1FTBW2XG9KE123456',
        make='Mercedes-Benz',
        model='Sprinter',
        sub_model='2500',
        series='High Roof',
        year=2022,
        body_type='Van',
        drive_type='RWD',
        fuel_type='Diesel',
        transmission='Automatic',
        engine_spec='2.0L 4-cylinder 161 hp',
        doors=4,
        chassis_no='MBZ2022F24680',
        color='White',
        odometer_reading=55000,
        notes='Delivery vehicle. Needs regular oil changes.',
        active=True
    )
    
    db.session.add_all([vehicle1, vehicle2, vehicle3, vehicle4, vehicle5])
    db.session.commit()
    
    # ========== LEADS ==========
    lead1 = Leads(
        full_name='David Johnson',
        email='david.johnson@gmail.com',
        phone='555-1111',
        rego='BEST-123',
        rego_state='TX',
        vehicle_description='2022 Ford Mustang GT',
        address='123 Race Track Road',
        notes='Looking to sell or trade in. Needs valuation ASAP.'
    )
    
    lead2 = Leads(
        full_name='Jennifer Lee',
        email='jen.lee@yahoo.com',
        phone='555-2222',
        rego='SUN-789',
        rego_state='FL',
        vehicle_description='2020 BMW 3 Series 330i',
        address='456 Beach Boulevard',
        notes='Considering upgrading to an SUV. Wants test drive options.'
    )
    
    lead3 = Leads(
        full_name='Michael Brown',
        email='michael.brown@work.com',
        phone='555-3333',
        rego='WORK-456',
        rego_state='NY',
        vehicle_description='2021 Chevrolet Silverado 1500',
        address='789 Business Park Drive',
        notes='Fleet inquiry. Looking to purchase 5 vehicles.'
    )
    
    lead4 = Leads(
        full_name='Amanda Martinez',
        email='amanda.martinez@hotmail.com',
        phone='555-4444',
        rego='GREEN-22',
        rego_state='CA',
        vehicle_description='2023 Hyundai Ioniq 5 Electric',
        address='321 Eco Street',
        notes='First-time EV buyer. Needs education on charging and incentives.'
    )
    
    lead5 = Leads(
        full_name='James Wilson',
        email='jwilson@outlook.com',
        phone='555-5555',
        rego='CLASSIC',
        rego_state='MI',
        vehicle_description='1969 Ford Mustang Fastback',
        address='654 Heritage Drive',
        notes='Classic car owner. Looking for specialty insurance and storage.'
    )
    
    db.session.add_all([lead1, lead2, lead3, lead4, lead5])
    db.session.commit()
    
    print(f"✅ Seeded: {Customer.query.count()} customers, {Vehicle.query.count()} vehicles, {Leads.query.count()} leads")


if __name__ == '__main__':
    app = create_app()
    app.logger.setLevel(logging.INFO)
    app.run(debug=True, host='0.0.0.0', port=5000)
