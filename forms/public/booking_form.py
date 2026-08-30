from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class BookingForm(FlaskForm):
    full_name = StringField('FULL NAME', validators=[DataRequired(), Length(max=100)])
    phone = StringField('PHONE', validators=[DataRequired(), Length(max=20)])
    email = StringField('EMAIL', validators=[DataRequired(), Email()])
    rego = StringField('rego', validators=[DataRequired(), Length(max=10)])
    rego_state = SelectField('rego_state', choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('WA', 'WA'), ('SA', 'SA'), ('TAS', 'TAS'), ('NT', 'NT'), ('ACT', 'ACT')], validators=[DataRequired()])
    vehicle_description = StringField('VEHICLE DESCRIPTION', validators=[DataRequired(), Length(max=200)])
    address = StringField('SERVICE ADDRESS', validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField('NOTES', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Request Booking')