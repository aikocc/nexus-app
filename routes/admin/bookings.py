from database import db, Booking, Lead
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

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    street = request.form.get('street')
    suburb = request.form.get('suburb')
    state = request.form.get('state')
    postcode = request.form.get('postcode')

    booking = Booking.query.get_or_404()
    return render_template('admin_booking_detail.html', booking=booking)


@booking_bp.get('/booking/new')
@login_required
def admin_booking_new_page(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('admin_booking_detail.html', booking=booking)


@booking_bp.route('/booking/<int:booking_id>')
@login_required
def admin_booking_detail(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('admin_booking_detail.html', booking=booking)


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
