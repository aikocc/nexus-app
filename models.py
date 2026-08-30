from datetime import datetime
from extensions import db


class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(150), nullable=True)
    email = db.Column(db.String(255), nullable=True, index=True)
    phone = db.Column(db.String(20), nullable=True)
    mobile = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(100), nullable=True)
    tax_id = db.Column(db.String(50), nullable=True)
    is_company = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vehicles = db.relationship('Vehicle', back_populates='customer', 
                               cascade='all, delete-orphan', lazy='dynamic')

    @property
    def full_name(self):
        name = f"{self.first_name} {self.last_name}"
        if self.company_name:
            name += f" ({self.company_name})"
        return name

    @property
    def vehicle_count(self):
        return self.vehicles.count()

    def __repr__(self):
        return f"<Customer {self.full_name}>"


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), 
                           nullable=False, index=True)
    
    # Registration Details
    registration_no = db.Column(db.String(20), nullable=False, unique=True, index=True)
    rego_state = db.Column(db.String(10), nullable=True)
    vin = db.Column(db.String(17), nullable=True, unique=True, index=True)
    
    # Vehicle Identification
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    sub_model = db.Column(db.String(100), nullable=True)
    series = db.Column(db.String(50), nullable=True)
    
    # Vehicle Specifications
    year = db.Column(db.Integer, nullable=True)
    body_type = db.Column(db.String(50), nullable=True)
    drive_type = db.Column(db.String(20), nullable=True)
    fuel_type = db.Column(db.String(20), nullable=True)
    transmission = db.Column(db.String(20), nullable=True)
    engine_spec = db.Column(db.String(200), nullable=True)
    doors = db.Column(db.Integer, nullable=True)
    
    # Chassis
    chassis_no = db.Column(db.String(50), nullable=True)
    
    # Manual Entry Fields
    color = db.Column(db.String(50), nullable=True)
    odometer_reading = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    active = db.Column(db.Boolean, default=True)
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='vehicles')

    @property
    def full_description(self):
        parts = []
        if self.year:
            parts.append(str(self.year))
        parts.extend([self.make, self.model])
        if self.sub_model:
            parts.append(self.sub_model)
        if self.registration_no:
            parts.append(f"({self.registration_no})")
        return " ".join(parts)

    def __repr__(self):
        return f"<Vehicle {self.registration_no}>"


class Leads(db.Model):
    __tablename__ = "leads"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    rego = db.Column(db.String(10), nullable=False)
    rego_state = db.Column(db.String(4), nullable=False)
    vehicle_description = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text, nullable=False)

    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"<Lead {self.full_name} - {self.phone} - {self.rego}>"