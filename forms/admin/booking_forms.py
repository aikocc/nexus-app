# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateField, TimeField
# from wtforms.validators import DataRequired, Email, Optional, Length, NumberRange

# class BookingForm(FlaskForm):
#     # Customer Info
#     customer_search = StringField('Search Customer')  # For autocomplete
#     customer_name = StringField('Customer Name', validators=[DataRequired(), Length(max=200)])
#     customer_email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
#     customer_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
#     customer_address = TextAreaField('Address', validators=[Optional()])
#     customer_suburb = StringField('Suburb', validators=[Optional(), Length(max=100)])
#     customer_postcode = StringField('Postcode', validators=[Optional(), Length(max=10)])
    
#     # Vehicle Info
#     vehicle_search = StringField('Search Vehicle')  # For autocomplete
#     vehicle_rego = StringField('Registration', validators=[Optional(), Length(max=20)])
#     vehicle_rego_state = StringField('State', validators=[Optional(), Length(max=50)])
#     vehicle_vin = StringField('VIN', validators=[Optional(), Length(max=17)])
#     vehicle_make = StringField('Make', validators=[Optional(), Length(max=50)])
#     vehicle_model = StringField('Model', validators=[Optional(), Length(max=50)])
#     vehicle_year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2026)])
#     vehicle_description = TextAreaField('Vehicle Description', validators=[Optional()])
    
#     # Service Details
#     service_type = SelectField('Service Type', validators=[DataRequired()], choices=[
#         ('engine_scan', 'Engine Code Scan - $79'),
#         ('brake_inspection', 'Brake Inspection - $89'),
#         ('battery_test', 'Battery Test - $59'),
#         ('full_health_report', 'Full Health Report - $149'),
#         ('ac_diagnostics', 'AC Diagnostics - $99'),
#         ('sensor_mapping', 'Sensor Mapping - $129')
#     ])
#     service_description = TextAreaField('Service Description', validators=[Optional()])
#     customer_notes = TextAreaField('Customer Notes', validators=[Optional()])
#     special_instructions = TextAreaField('Special Instructions', validators=[Optional()])
    
#     # Scheduling
#     preferred_date = DateField('Preferred Date', format='%Y-%m-%d', validators=[Optional()])
#     preferred_time_slot = SelectField('Preferred Time', choices=[
#         ('morning', 'Morning (8am - 12pm)'),
#         ('afternoon', 'Afternoon (12pm - 5pm)'),
#         ('evening', 'Evening (5pm - 8pm)'),
#         ('any', 'Any Time')
#     ], validators=[Optional()])
#     scheduled_date = DateField('Scheduled Date', format='%Y-%m-%d', validators=[Optional()])
#     scheduled_time = TimeField('Scheduled Time', format='%H:%M', validators=[Optional()])
#     duration_minutes = IntegerField('Duration (minutes)', default=60, validators=[Optional()])
    
#     # Status
#     status = SelectField('Status', choices=[
#         ('pending', 'Pending'),
#         ('confirmed', 'Confirmed'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#         ('no_show', 'No Show')
#     ], validators=[DataRequired()])
#     priority = SelectField('Priority', choices=[
#         ('low', 'Low'),
#         ('normal', 'Normal'),
#         ('high', 'High'),
#         ('urgent', 'Urgent')
#     ], validators=[DataRequired()])
    
#     # Location
#     service_address = TextAreaField('Service Address', validators=[Optional()])
#     service_suburb = StringField('Service Suburb', validators=[Optional(), Length(max=100)])
#     service_postcode = StringField('Service Postcode', validators=[Optional(), Length(max=10)])





from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, SelectField, IntegerField, 
    DateField, TimeField, HiddenField, SubmitField
)
from wtforms.validators import DataRequired, Optional, Email, Length, NumberRange
from datetime import datetime


class BookingForm(FlaskForm):
    """Form for creating and editing bookings"""
    
    # ============================================
    # Customer Information
    # ============================================
    customer_search = HiddenField('Customer Search')
    customer_name = StringField(
        'Customer Name',
        validators=[DataRequired(message='Customer name is required'), Length(max=200)]
    )
    customer_email = StringField(
        'Email',
        validators=[Optional(), Email(message='Invalid email address'), Length(max=120)]
    )
    customer_phone = StringField(
        'Phone',
        validators=[Optional(), Length(max=20)]
    )
    customer_address = TextAreaField(
        'Address',
        validators=[Optional(), Length(max=500)]
    )
    customer_suburb = StringField(
        'Suburb',
        validators=[Optional(), Length(max=100)]
    )
    customer_postcode = StringField(
        'Postcode',
        validators=[Optional(), Length(max=10)]
    )
    
    # ============================================
    # Vehicle Information
    # ============================================
    vehicle_search = HiddenField('Vehicle Search')
    vehicle_rego = StringField(
        'Registration',
        validators=[DataRequired(message='Registration is required'), Length(max=20)]
    )
    vehicle_rego_state = StringField(
        'Rego State',
        validators=[Optional(), Length(max=10)]
    )
    vehicle_vin = StringField(
        'VIN',
        validators=[Optional(), Length(max=17)]
    )
    vehicle_make = StringField(
        'Make',
        validators=[DataRequired(message='Make is required'), Length(max=50)]
    )
    vehicle_model = StringField(
        'Model',
        validators=[DataRequired(message='Model is required'), Length(max=50)]
    )
    vehicle_year = IntegerField(
        'Year',
        validators=[Optional(), NumberRange(min=1900, max=datetime.now().year + 1)]
    )
    vehicle_description = TextAreaField(
        'Vehicle Description',
        validators=[Optional(), Length(max=500)]
    )
    
    # ============================================
    # Service Details
    # ============================================
    service_type = SelectField(
        'Service Type',
        choices=[
            ('', 'Select Service Type'),
            ('engine_scan', 'Engine Scan'),
            ('diagnostic_test', 'Diagnostic Test'),
            ('oil_change', 'Oil Change'),
            ('brake_service', 'Brake Service'),
            ('transmission_service', 'Transmission Service'),
            ('battery_test', 'Battery Test'),
            ('wheel_alignment', 'Wheel Alignment'),
            ('aircon_service', 'Aircon Service'),
            ('major_service', 'Major Service'),
            ('minor_service', 'Minor Service'),
            ('engine_repair', 'Engine Repair'),
            ('electrical_diagnostic', 'Electrical Diagnostic')
        ],
        validators=[DataRequired(message='Service type is required')]
    )
    service_description = TextAreaField(
        'Service Description',
        validators=[Optional(), Length(max=500)]
    )
    duration_minutes = IntegerField(
        'Duration (minutes)',
        validators=[Optional(), NumberRange(min=15, max=480)],
        default=60
    )
    
    # ============================================
    # Customer Notes
    # ============================================
    customer_notes = TextAreaField(
        'Customer Notes',
        validators=[Optional(), Length(max=1000)]
    )
    special_instructions = TextAreaField(
        'Special Instructions',
        validators=[Optional(), Length(max=1000)]
    )
    
    # ============================================
    # Scheduling
    # ============================================
    preferred_date = DateField(
        'Preferred Date',
        validators=[Optional()]
    )
    preferred_time_slot = StringField(
        'Preferred Time Slot',
        validators=[Optional(), Length(max=50)]
    )
    scheduled_date = DateField(
        'Scheduled Date',
        validators=[Optional()]
    )
    scheduled_time = TimeField(
        'Scheduled Time',
        validators=[Optional()]
    )
    
    # ============================================
    # Status & Priority
    # ============================================
    status = SelectField(
        'Status',
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show')
        ],
        default='pending'
    )
    priority = SelectField(
        'Priority',
        choices=[
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('urgent', 'Urgent')
        ],
        default='normal'
    )
    
    # ============================================
    # Service Location
    # ============================================
    service_address = TextAreaField(
        'Service Address',
        validators=[Optional(), Length(max=500)]
    )
    service_suburb = StringField(
        'Service Suburb',
        validators=[Optional(), Length(max=100)]
    )
    service_postcode = StringField(
        'Service Postcode',
        validators=[Optional(), Length(max=10)]
    )
    
    # ============================================
    # Hidden Fields
    # ============================================
    lead_id = HiddenField('Lead ID')
    
    # ============================================
    # Submit
    # ============================================
    submit = SubmitField('Save Booking')
    
    def validate_scheduled_date(self, field):
        """Validate that scheduled date is not in the past (unless editing)"""
        if field.data and field.data < datetime.now().date():
            # Allow past dates when editing (will be handled in route)
            pass
        return True
    
    def validate_duration_minutes(self, field):
        """Validate duration is reasonable"""
        if field.data and field.data > 480:
            raise ValueError('Duration cannot exceed 480 minutes (8 hours)')
        return True


class BookingSearchForm(FlaskForm):
    """Form for searching bookings"""
    search = StringField('Search', validators=[Optional(), Length(max=100)])
    status = SelectField(
        'Status',
        choices=[
            ('', 'All Status'),
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show')
        ],
        validators=[Optional()]
    )
    priority = SelectField(
        'Priority',
        choices=[
            ('', 'All Priority'),
            ('low', 'Low'),
            ('normal', 'Normal'),
            ('high', 'High'),
            ('urgent', 'Urgent')
        ],
        validators=[Optional()]
    )
    date_from = DateField('From Date', validators=[Optional()])
    date_to = DateField('To Date', validators=[Optional()])
    submit = SubmitField('Filter')
    
    def validate_date_range(self):
        """Validate that date_from is not after date_to"""
        if self.date_from.data and self.date_to.data:
            if self.date_from.data > self.date_to.data:
                raise ValueError('From date cannot be after To date')
        return True


class BookingQuickForm(FlaskForm):
    """Quick booking form for rapid entry"""
    customer_name = StringField(
        'Customer Name',
        validators=[DataRequired(message='Customer name is required'), Length(max=200)]
    )
    customer_phone = StringField(
        'Phone',
        validators=[DataRequired(message='Phone is required'), Length(max=20)]
    )
    vehicle_rego = StringField(
        'Registration',
        validators=[DataRequired(message='Registration is required'), Length(max=20)]
    )
    vehicle_make = StringField(
        'Make',
        validators=[DataRequired(message='Make is required'), Length(max=50)]
    )
    vehicle_model = StringField(
        'Model',
        validators=[DataRequired(message='Model is required'), Length(max=50)]
    )
    service_type = SelectField(
        'Service Type',
        choices=[
            ('engine_scan', 'Engine Scan'),
            ('diagnostic_test', 'Diagnostic Test'),
            ('oil_change', 'Oil Change'),
            ('brake_service', 'Brake Service'),
            ('battery_test', 'Battery Test'),
            ('wheel_alignment', 'Wheel Alignment')
        ],
        validators=[DataRequired(message='Service type is required')]
    )
    scheduled_date = DateField(
        'Scheduled Date',
        validators=[DataRequired(message='Scheduled date is required')]
    )
    scheduled_time = TimeField(
        'Scheduled Time',
        validators=[DataRequired(message='Scheduled time is required')]
    )
    notes = TextAreaField(
        'Notes',
        validators=[Optional(), Length(max=500)]
    )
    submit = SubmitField('Quick Book')