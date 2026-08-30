from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, NumberRange


class VehicleForm(FlaskForm):
    """Form for admin to create/edit vehicles"""
    
    # Customer (hidden ID + searchable text field)
    customer_id = HiddenField('Customer ID', validators=[DataRequired()])
    customer_search = StringField('Customer *', validators=[DataRequired()], 
                                  description="Search by name, email, or phone")
    
    # Registration Details
    registration_no = StringField('Registration No *', validators=[DataRequired(), Length(max=20)])
    rego_state = StringField('State', validators=[Optional(), Length(max=10)])
    vin = StringField('VIN', validators=[Optional(), Length(max=17)])
    
    # Vehicle Identification
    make = StringField('Make *', validators=[DataRequired(), Length(max=100)])
    model = StringField('Model *', validators=[DataRequired(), Length(max=100)])
    sub_model = StringField('Sub Model', validators=[Optional(), Length(max=100)])
    series = StringField('Series', validators=[Optional(), Length(max=50)])
    
    # Vehicle Specifications
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2100)])
    body_type = SelectField('Body Type', choices=[
        ('', 'Select Body Type'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Ute', 'Ute'),
        ('Hatchback', 'Hatchback'),
        ('Wagon', 'Wagon'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
        ('Van', 'Van'),
        ('Minibus', 'Minibus'),
        ('Truck', 'Truck'),
        ('Other', 'Other')
    ], validators=[Optional()])
    
    drive_type = SelectField('Drive Type', choices=[
        ('', 'Select Drive Type'),
        ('FWD', 'FWD'),
        ('RWD', 'RWD'),
        ('AWD', 'AWD'),
        ('4WD', '4WD'),
        ('2WD', '2WD')
    ], validators=[Optional()])
    
    fuel_type = SelectField('Fuel Type', choices=[
        ('', 'Select Fuel Type'),
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('BEV', 'Electric (BEV)'),
        ('PHEV', 'Plug-in Hybrid'),
        ('HYBRID', 'Hybrid'),
        ('LPG', 'LPG'),
        ('OTHER', 'Other')
    ], validators=[Optional()])
    
    transmission = SelectField('Transmission', choices=[
        ('', 'Select Transmission'),
        ('Auto', 'Auto'),
        ('Manual', 'Manual'),
        ('Auto/Manual', 'Auto/Manual'),
        ('CVT', 'CVT'),
        ('Other', 'Other')
    ], validators=[Optional()])
    
    engine_spec = StringField('Engine Spec', validators=[Optional(), Length(max=200)])
    doors = SelectField('Doors', choices=[
        ('', 'Select'),
        (2, '2 Doors'),
        (3, '3 Doors'),
        (4, '4 Doors'),
        (5, '5 Doors')
    ], coerce=int, validators=[Optional()])
    
    # Chassis
    chassis_no = StringField('Chassis No', validators=[Optional(), Length(max=50)])
    
    # Manual Entry Fields
    color = StringField('Color', validators=[Optional(), Length(max=50)])
    odometer_reading = IntegerField('Odometer (km)', validators=[Optional(), NumberRange(min=0)])
    notes = TextAreaField('Notes', validators=[Optional()])
    
    submit = SubmitField('Save Vehicle')


class RegoLookupForm(FlaskForm):
    """Form for rego lookup"""
    rego = StringField('Registration Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Lookup')