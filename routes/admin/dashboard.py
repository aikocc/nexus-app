from database import db, Booking, Lead
from decorators import login_required

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # pyright: ignore[reportMissingImports]

admin_dashboard_bp = Blueprint("admin_dashboard", __name__, url_prefix="/admin", template_folder='templates')

@admin_dashboard_bp.route('')
@login_required
def admin_dashboard():
    status_filter = request.args.get('status', 'all')
    leads_arg = request.args.get('q', False)

    booking_query = Booking.query.order_by(Booking.created_at.desc())
    if status_filter != 'all':
        booking_query = booking_query.filter_by(status=status_filter)
    bookings_result = booking_query.all()

    counts = {
        'all':          Booking.query.count(),
        'pending':      Booking.query.filter_by(status='pending').count(),
        'confirmed':    Booking.query.filter_by(status='confirmed').count(),
        'in_progress':  Booking.query.filter_by(status='in_progress').count(),
        'completed':    Booking.query.filter_by(status='completed').count(),
        'cancelled':    Booking.query.filter_by(status='cancelled').count(),
        'leads':        Lead.query.count(),
    }


    leads_query = Lead.query.order_by(Lead.created_at.desc())
    leads = leads_query.all()

    print(leads, bookings_result)

    return render_template('admin_dashboard.html',
                           bookings=bookings_result, leads=leads,
                           counts=counts, active_filter=('leads' if leads_arg != False else status_filter))