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
    bookings = db.relationship('Booking', back_populates='customer', lazy=True)

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
    
    registration_no = db.Column(db.String(20), nullable=False, unique=True, index=True)
    rego_state = db.Column(db.String(10), nullable=True)
    vin = db.Column(db.String(17), nullable=True, unique=True, index=True)
    
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    sub_model = db.Column(db.String(100), nullable=True)
    series = db.Column(db.String(50), nullable=True)
    
    year = db.Column(db.Integer, nullable=True)
    body_type = db.Column(db.String(50), nullable=True)
    drive_type = db.Column(db.String(20), nullable=True)
    fuel_type = db.Column(db.String(20), nullable=True)
    transmission = db.Column(db.String(20), nullable=True)
    engine_spec = db.Column(db.String(200), nullable=True)
    doors = db.Column(db.Integer, nullable=True)
    
    chassis_no = db.Column(db.String(50), nullable=True)
    
    color = db.Column(db.String(50), nullable=True)
    odometer_reading = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='vehicles')
    bookings = db.relationship('Booking', back_populates='vehicle', lazy=True)

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


class Lead(db.Model):
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

    converted = db.Column(db.Boolean, default=False)
    converted_at = db.Column(db.DateTime)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id', ondelete='SET NULL'), nullable=True)
    
    # The backref 'booking' is created by the relationship in Booking model
    # No need to define it here

    def __repr__(self):
        return f"<Lead {self.full_name} - {self.phone} - {self.rego}>"


class Booking(db.Model):
    __tablename__ = 'bookings'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    booking_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Foreign Keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='SET NULL'), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='SET NULL'), nullable=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id', ondelete='SET NULL'), nullable=True)
    
    # Customer Snapshot
    customer_name = db.Column(db.String(200), nullable=False)
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20))
    customer_address = db.Column(db.Text)
    customer_suburb = db.Column(db.String(100))
    customer_postcode = db.Column(db.String(10))
    
    # Vehicle Snapshot
    vehicle_rego = db.Column(db.String(20))
    vehicle_rego_state = db.Column(db.String(50))
    vehicle_vin = db.Column(db.String(17))
    vehicle_make = db.Column(db.String(50))
    vehicle_model = db.Column(db.String(50))
    vehicle_year = db.Column(db.Integer)
    vehicle_description = db.Column(db.Text)
    
    # Service Details
    service_type = db.Column(db.String(50), nullable=False)
    service_description = db.Column(db.Text)
    customer_notes = db.Column(db.Text)
    special_instructions = db.Column(db.Text)
    
    # Scheduling
    preferred_date = db.Column(db.Date)
    preferred_time_slot = db.Column(db.String(50))
    scheduled_date = db.Column(db.Date)
    scheduled_time = db.Column(db.Time)
    duration_minutes = db.Column(db.Integer, default=60)
    
    # Status
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='normal')
    
    # Location
    service_address = db.Column(db.Text)
    service_suburb = db.Column(db.String(100))
    service_postcode = db.Column(db.String(10))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Relationships - FIXED: Specify foreign_keys for lead
    customer = db.relationship('Customer', back_populates='bookings', lazy=True)
    vehicle = db.relationship('Vehicle', back_populates='bookings', lazy=True)
    lead = db.relationship(
        'Lead', 
        foreign_keys=[lead_id],  # Explicitly specify which foreign key to use
        backref='booking',       # Creates Lead.booking attribute
        lazy=True
    )
    
    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
    
    def generate_booking_number(self):
        """Generate a unique booking number: BK-YYYYMMDD-XXXX"""
        now = datetime.utcnow()
        date_part = now.strftime('%Y%m%d')
        today_count = Booking.query.filter(
            Booking.created_at >= now.replace(hour=0, minute=0, second=0)
        ).count()
        return f"BK-{date_part}-{str(today_count + 1).zfill(4)}"
    
    def link_to_customer(self, customer):
        """Link booking to an existing customer"""
        if customer:
            self.customer_id = customer.id
            self.customer_name = f"{customer.first_name} {customer.last_name}"
            self.customer_email = customer.email
            self.customer_phone = customer.phone
            self.customer_address = customer.address
            db.session.commit()
            return True
        return False
    
    def link_to_vehicle(self, vehicle):
        """Link booking to an existing vehicle"""
        if vehicle:
            self.vehicle_id = vehicle.id
            self.vehicle_rego = vehicle.registration_no
            self.vehicle_rego_state = vehicle.rego_state
            self.vehicle_vin = vehicle.vin
            self.vehicle_make = vehicle.make
            self.vehicle_model = vehicle.model
            self.vehicle_year = vehicle.year
            db.session.commit()
            return True
        return False
    
    def sync_from_lead(self, lead):
        """Populate booking from a lead object"""
        if lead:
            self.lead_id = lead.id
            self.customer_name = lead.full_name
            self.customer_email = lead.email
            self.customer_phone = lead.phone
            self.customer_address = lead.address
            self.vehicle_rego = lead.rego
            self.vehicle_rego_state = lead.rego_state
            self.vehicle_description = lead.vehicle_description
            self.customer_notes = lead.notes
            db.session.commit()
    
    def confirm(self):
        """Mark booking as confirmed"""
        self.status = 'confirmed'
        self.confirmed_at = datetime.utcnow()
        db.session.commit()
    
    def complete(self):
        """Mark booking as completed"""
        self.status = 'completed'
        self.completed_at = datetime.utcnow()
        db.session.commit()
    
    def cancel(self):
        """Mark booking as cancelled"""
        self.status = 'cancelled'
        self.cancelled_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            'id': self.id,
            'booking_number': self.booking_number,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_phone': self.customer_phone,
            'vehicle_rego': self.vehicle_rego,
            'vehicle_make': self.vehicle_make,
            'vehicle_model': self.vehicle_model,
            'service_type': self.service_type,
            'status': self.status,
            'preferred_date': self.preferred_date.isoformat() if self.preferred_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Booking {self.booking_number} - {self.customer_name}>'