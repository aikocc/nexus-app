from database import Customer, Vehicle, db, Booking, Lead
from decorators import login_required

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # pyright: ignore[reportMissingImports]

booking_bp = Blueprint("booking", __name__, url_prefix="/admin", template_folder='templates')


@booking_bp.route('/lead/<int:lead_id>')
@login_required
def admin_lead_detail(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    return render_template('admin_lead_detail.html', lead=lead)

@booking_bp.route('/lead/<int:lead_id>/status', methods=['POST'])
@login_required
def admin_update_lead_status(lead_id):
    lead    = Lead.query.get_or_404(lead_id)
    new_status = request.form.get('status')
    valid      = {'pending', 'confirmed', 'in_progress', 'completed', 'cancelled'}
    if new_status not in valid:
        flash('Invalid status.', 'error')
    else:
        lead.status = new_status
        db.session.commit()
        flash(f'Lead #{lead.id} updated to {new_status.replace("_", " ")}.', 'success')
    return redirect(url_for('admin_lead_detail', lead_id=lead_id))

@booking_bp.route('/lead/<int:lead_id>/delete', methods=['POST'])
@login_required
def admin_delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    flash(f'Lead #{lead_id} deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


@booking_bp.post('/booking/new')
@login_required
def admin_booking_convert_lead():

    customer_id = request.form.get('customer_id')

    if customer_id:
        customer = Customer.query.get_or_404(customer_id)
    else:
        customer = Customer(
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            street=request.form.get('street'),
            suburb=request.form.get('suburb'),
            state=request.form.get('state'),
            postcode=request.form.get('postcode')
        )
        db.session.add(customer)
        db.session.commit()

    vehicle_id = request.form.get('vehicle_id')
    if vehicle_id:
        vehicle = Vehicle.query.get_or_404(vehicle_id)
    else:
        vehicle = Vehicle(
            make=request.form.get('make'),
            model=request.form.get('model'),
            series=request.form.get('series'),
            year=request.form.get('year'),
            rego=request.form.get('rego'),
            rego_state=request.form.get('rego_state'),
            vin=request.form.get('vin')
        )
        db.session.add(vehicle)
        db.session.commit()

    booking = Booking(
        customer_id=customer.id,
        vehicle_id=vehicle.id,
        service=request.form.get('service'),
        urgency=request.form.get('urgency'),
        address=request.form.get('address'),
        notes=request.form.get('notes'),
        status='pending'
    )
    db.session.add(booking)
    db.session.commit()

    booking = Booking.query.get_or_404(booking.id)
    return redirect(url_for('admin_booking_detail', booking_id=booking.id, saved='Booking created successfully.'))

@booking_bp.get('/booking/new')
@login_required
def admin_booking_new_page(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('admin_booking_detail.html', booking=booking)


@booking_bp.route('/booking/<int:booking_id>')
@login_required
def admin_booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    customer = Customer.query.get(booking.customer_id)
    vehicle = Vehicle.query.get(booking.vehicle_id)
    last_odometer = vehicle.last_odometer if vehicle else None
    last_odometer_date = vehicle.last_odometer_date if vehicle else None
    current_odometer = request.args.get('current_odometer', None)
    vehicle_notes = vehicle.notes if vehicle else None
    customer_history = Booking.query.filter_by(customer_id=booking.customer_id).order_by(Booking.created_at.desc()).all() if customer else []
    vehicle_history = Booking.query.filter_by(vehicle_id=booking.vehicle_id).order_by(Booking.created_at.desc()).all() if vehicle else []
    customer_lifetime_spend = sum(inv.total_amount for inv in booking.invoices) if booking.invoices else 0.0

    return render_template('admin_booking_overview.html',
    booking=booking, customer=customer, vehicle=vehicle,
    last_odometer=last_odometer, last_odometer_date=last_odometer_date, current_odometer=current_odometer,
    vehicle_notes=vehicle_notes, customer_history=customer_history, vehicle_history=vehicle_history,
    customer_lifetime_spend=customer_lifetime_spend)


@booking_bp.route('/booking/<int:booking_id>/status', methods=['POST'])
@login_required
def admin_update_booking_status(booking_id):
    booking    = Booking.query.get_or_404(booking_id)
    new_status = request.form.get('status')
    valid      = {'pending', 'confirmed', 'in_progress', 'completed', 'cancelled'}
    if new_status not in valid:
        flash('Invalid status.', 'error')
    else:
        booking.status = new_status
        db.session.commit()
        flash(f'Booking #{booking.id} updated to {new_status.replace("_", " ")}.', 'success')
    return redirect(url_for('admin_booking_detail', booking_id=booking_id))


@booking_bp.route('/booking/<int:booking_id>/delete', methods=['POST'])
@login_required
def admin_delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash(f'Booking #{booking_id} deleted.', 'success')
    return redirect(url_for('admin_dashboard'))
