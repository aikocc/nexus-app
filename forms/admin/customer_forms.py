from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class CustomerForm(FlaskForm):
    """Form for admin to create/edit customers"""
    first_name = StringField('First Name *', validators=[DataRequired(), Length(max=100)])
    last_name = StringField('Last Name *', validators=[DataRequired(), Length(max=100)])
    company_name = StringField('Company', validators=[Optional(), Length(max=150)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=255)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    mobile = StringField('Mobile', validators=[Optional(), Length(max=20)])
    address = TextAreaField('Address', validators=[Optional()])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    state = StringField('State', validators=[Optional(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[Optional(), Length(max=20)])
    country = StringField('Country', validators=[Optional(), Length(max=100)])
    tax_id = StringField('Tax ID / VAT', validators=[Optional(), Length(max=50)])
    is_company = BooleanField('Is Company?')
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Customer')