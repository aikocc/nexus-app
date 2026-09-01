from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange

class BookingForm(FlaskForm):
    # Customer Info
    customer_search = StringField('Search Customer')  # For autocomplete
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=200)])
    customer_email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    customer_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    customer_address = TextAreaField('Address', validators=[Optional()])
    customer_suburb = StringField('Suburb', validators=[Optional(), Length(max=100)])
    customer_postcode = StringField('Postcode', validators=[Optional(), Length(max=10)])
    
    # Vehicle Info
    vehicle_search = StringField('Search Vehicle')  # For autocomplete
    vehicle_rego = StringField('Registration', validators=[Optional(), Length(max=20)])
    vehicle_rego_state = StringField('State', validators=[Optional(), Length(max=50)])
    vehicle_vin = StringField('VIN', validators=[Optional(), Length(max=17)])
    vehicle_make = StringField('Make', validators=[Optional(), Length(max=50)])
    vehicle_model = StringField('Model', validators=[Optional(), Length(max=50)])
    vehicle_year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2026)])
    vehicle_description = TextAreaField('Vehicle Description', validators=[Optional()])
    
    # Service Details
    service_type = SelectField('Service Type', validators=[DataRequired()], choices=[
        ('engine_scan', 'Engine Code Scan - $79'),
        ('brake_inspection', 'Brake Inspection - $89'),
        ('battery_test', 'Battery Test - $59'),
        ('full_health_report', 'Full Health Report - $149'),
        ('ac_diagnostics', 'AC Diagnostics - $99'),
        ('sensor_mapping', 'Sensor Mapping - $129')
    ])
    service_description = TextAreaField('Service Description', validators=[Optional()])
    customer_notes = TextAreaField('Customer Notes', validators=[Optional()])
    special_instructions = TextAreaField('Special Instructions', validators=[Optional()])
    
    # Scheduling
    preferred_date = DateField('Preferred Date', format='%Y-%m-%d', validators=[Optional()])
    preferred_time_slot = SelectField('Preferred Time', choices=[
        ('morning', 'Morning (8am - 12pm)'),
        ('afternoon', 'Afternoon (12pm - 5pm)'),
        ('evening', 'Evening (5pm - 8pm)'),
        ('any', 'Any Time')
    ], validators=[Optional()])
    scheduled_date = DateField('Scheduled Date', format='%Y-%m-%d', validators=[Optional()])
    scheduled_time = TimeField('Scheduled Time', format='%H:%M', validators=[Optional()])
    duration_minutes = IntegerField('Duration (minutes)', default=60, validators=[Optional()])
    
    # Status
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], validators=[DataRequired()])
    
    # Location
    service_address = TextAreaField('Service Address', validators=[Optional()])
    service_suburb = StringField('Service Suburb', validators=[Optional(), Length(max=100)])
    service_postcode = StringField('Service Postcode', validators=[Optional(), Length(max=10)])