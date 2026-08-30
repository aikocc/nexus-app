from flask import Blueprint, render_template

customer_appointments_bp = Blueprint('customer_appointments', __name__, url_prefix='/customer/appointments')


@customer_appointments_bp.route('/')
def my_appointments():
    appointments = []
    return render_template('customer/appointments.html', appointments=appointments)
