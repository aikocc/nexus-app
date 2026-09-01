from flask import Blueprint, render_template

from forms.public.booking_form import BookingForm
from flask import request, jsonify, flash, redirect, url_for
from extensions import db
from models import Lead

public_bp = Blueprint('public', __name__)


@public_bp.route('/')
def index():
    form = BookingForm()
    return render_template('public/index.html', form=form)


@public_bp.route('/about')
def about():
    return render_template('public/about.html')


@public_bp.route('/contact')
def contact():
    return render_template('public/contact.html')


@public_bp.route('/book', methods=['GET', 'POST'])
def create_booking():
    form = BookingForm()
    
    if form.validate_on_submit():
        # Process the booking
        booking_data = {
            'full_name': form.full_name.data,
            'phone': form.phone.data,
            'email': form.email.data,
            'rego': form.rego.data,
            'rego_state': form.rego_state.data,
            'vehicle_description': form.vehicle_description.data,
            'address': form.address.data,
            'notes': form.notes.data
        }

        db.session.add(Lead(**booking_data))
        db.session.commit()
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': 'Booking request received! We will confirm within 24 hours.',
                'data': booking_data
            })
        
        # For regular form submission
        flash('Booking request received! We will confirm within 24 hours.', 'success')
        return redirect(url_for('public.create_booking'))
    
    # Handle AJAX form validation errors
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'POST':
        errors = {field: errors for field, errors in form.errors.items()}
        return jsonify({
            'success': False,
            'errors': errors
        }), 400
    
    return render_template('public/index.html', form=form)