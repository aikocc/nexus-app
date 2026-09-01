from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Email


class LeadForm(FlaskForm):
    '''Form to convert a lead into a booking or to edit lead details'''
    # Customer Details
    first_name = StringField('First Name', validators=[Optional(), Length(max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    phone = IntegerField('Phone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    suburb = StringField('Suburb', validators=[Optional(), Length(max=100)])
    postcode = IntegerField('Postcode', validators=[Optional(), Length(max=4)])

    # Vehicle Details
    rego = StringField('rego', validators=[Optional(), Length(max=10)])
    rego_state = SelectField('rego state', choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('WA', 'WA'), ('SA', 'SA'), ('TAS', 'TAS'), ('NT', 'NT'), ('ACT', 'ACT')], validators=[Optional()])
    vin = StringField('VIN', validators=[Optional(), Length(max=17)])
    make = StringField('Make', validators=[Optional(), Length(max=100)])
    model = StringField('Model', validators=[Optional(), Length(max=100)])
    series = StringField('Series', validators=[Optional(), Length(max=50)])
    year = IntegerField('Year', validators=[Optional(), NumberRange(min=1900, max=2100)])

    # Additional Details
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Convert to Booking')