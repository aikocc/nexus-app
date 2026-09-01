from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Booking, Customer, Vehicle, Lead
from forms.admin.booking_forms import BookingForm
from extensions import db
from datetime import datetime, timedelta
import calendar

admin_bookings_bp = Blueprint('admin_bookings', __name__, url_prefix='/admin/bookings')

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Booking, Customer, Vehicle, Lead
from forms.admin.booking_forms import BookingForm
from extensions import db
from datetime import datetime, timedelta
import calendar

admin_bookings_bp = Blueprint('admin_bookings', __name__, url_prefix='/admin/bookings')

@admin_bookings_bp.route('/')
def list_bookings():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Build query with filters
    query = Booking.query
    
    # Apply search filter
    search = request.args.get('search', '')
    if search:
        query = query.filter(
            db.or_(
                Booking.customer_name.ilike(f'%{search}%'),
                Booking.booking_number.ilike(f'%{search}%'),
                Booking.vehicle_rego.ilike(f'%{search}%'),
                Booking.vehicle_make.ilike(f'%{search}%'),
                Booking.vehicle_model.ilike(f'%{search}%'),
                Booking.customer_email.ilike(f'%{search}%'),
                Booking.customer_phone.ilike(f'%{search}%')
            )
        )
    
    # Apply status filter
    status = request.args.get('status', '')
    if status:
        query = query.filter_by(status=status)
    
    # Apply priority filter
    priority = request.args.get('priority', '')
    if priority:
        query = query.filter_by(priority=priority)
    
    # Apply date filters
    date_from = request.args.get('date_from', '')
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(Booking.scheduled_date >= from_date)
        except ValueError:
            pass
    
    date_to = request.args.get('date_to', '')
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            query = query.filter(Booking.scheduled_date <= to_date)
        except ValueError:
            pass
    
    # Order by created_at desc
    query = query.order_by(Booking.created_at.desc())
    
    # Paginate results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    bookings = pagination.items
    
    # Get stats
    stats = {
        'total': Booking.query.count(),
        'pending': Booking.query.filter_by(status='pending').count(),
        'confirmed': Booking.query.filter_by(status='confirmed').count(),
        'completed': Booking.query.filter_by(status='completed').count()
    }
    
    # Get view parameter
    view = request.args.get('view', 'list')
    
    # IMPORTANT: Get month and year from request parameters
    # Default to current date if not provided
    now = datetime.now()
    
    # Get month from request
    month_str = request.args.get('month', '')
    if month_str and month_str.isdigit():
        month = int(month_str)
        if month < 1 or month > 12:
            month = now.month
    else:
        month = now.month
    
    # Get year from request
    year_str = request.args.get('year', '')
    if year_str and year_str.isdigit():
        year = int(year_str)
        if year < 2000 or year > 2100:
            year = now.year
    else:
        year = now.year
    
    # Get calendar data for the requested month/year
    month_name = calendar.month_name[month]
    cal = calendar.monthcalendar(year, month)
    
    calendar_days = []
    for week in cal:
        for day in week:
            if day == 0:
                calendar_days.append({
                    'day': 0,
                    'is_today': False,
                    'is_current_month': False,
                    'booking_count': 0,
                    'bookings': []
                })
            else:
                date_obj = datetime(year, month, day)
                is_today = date_obj.date() == datetime.now().date()
                
                # Get bookings for this date
                day_bookings = Booking.query.filter(
                    db.func.date(Booking.scheduled_date) == date_obj.date()
                ).all()
                
                calendar_days.append({
                    'day': day,
                    'is_today': is_today,
                    'is_current_month': True,
                    'booking_count': len(day_bookings),
                    'bookings': day_bookings[:5]
                })
    
    # Previous and next month navigation
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year
    
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    
    # Debug logging
    print(f"=== CALENDAR DEBUG ===")
    print(f"View: {view}")
    print(f"Month from request: {month_str}")
    print(f"Year from request: {year_str}")
    print(f"Using month: {month}, year: {year}")
    print(f"Month name: {month_name}")
    print(f"Prev: {prev_month}/{prev_year}, Next: {next_month}/{next_year}")
    print(f"Next month: {next_month}, Next year: {next_year}")
    print(f"======================")
    
    # Check if HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    
    if is_htmx:
        return render_template(
            'admin/bookings/_booking_list_content.html',
            bookings=bookings,
            pagination=pagination,
            page=page,
            per_page=per_page,
            stats=stats,
            view=view,
            calendar_month=month_name,
            calendar_year=year,
            calendar_days=calendar_days,
            calendar_prev_month=prev_month,
            calendar_prev_year=prev_year,
            calendar_next_month=next_month,
            calendar_next_year=next_year,
            current_month=month,
            current_year=year
        )
    else:
        return render_template(
            'admin/bookings/list.html',
            bookings=bookings,
            pagination=pagination,
            page=page,
            per_page=per_page,
            stats=stats,
            view=view,
            calendar_month=month_name,
            calendar_year=year,
            calendar_days=calendar_days,
            calendar_prev_month=prev_month,
            calendar_prev_year=prev_year,
            calendar_next_month=next_month,
            calendar_next_year=next_year,
            current_month=month,
            current_year=year
        )

@admin_bookings_bp.route('/new', methods=['GET', 'POST'])
def new_booking():
    """Create a new booking"""
    form = BookingForm()
    
    # Pre-populate from lead if provided
    lead_id = request.args.get('lead_id')
    if lead_id and request.method == 'GET':
        lead = Lead.query.get(lead_id)
        if lead:
            form.customer_name.data = lead.full_name
            form.customer_email.data = lead.email
            form.customer_phone.data = lead.phone
            form.customer_address.data = lead.address
            form.vehicle_rego.data = lead.rego
            form.vehicle_rego_state.data = lead.rego_state
            form.vehicle_description.data = lead.vehicle_description
            form.customer_notes.data = lead.notes
            form.service_type.data = 'engine_scan'  # Default
    
    if form.validate_on_submit():
        booking = Booking()
        form.populate_obj(booking)
        
        # Try to link to existing customer
        customer = None
        if form.customer_search.data:
            try:
                customer_id = int(form.customer_search.data)
                customer = Customer.query.get(customer_id)
            except (ValueError, TypeError):
                pass
        else:
            # Try to find by email
            if form.customer_email.data:
                customer = Customer.query.filter_by(email=form.customer_email.data).first()
        
        if customer:
            booking.link_to_customer(customer)
        
        # Try to link to existing vehicle
        vehicle = None
        if form.vehicle_search.data:
            try:
                vehicle_id = int(form.vehicle_search.data)
                vehicle = Vehicle.query.get(vehicle_id)
            except (ValueError, TypeError):
                pass
        else:
            if form.vehicle_rego.data:
                vehicle = Vehicle.query.filter_by(registration_number=form.vehicle_rego.data).first()
        
        if vehicle:
            booking.link_to_vehicle(vehicle)
        
        db.session.add(booking)
        db.session.commit()
        
        flash('Booking created successfully!', 'success')
        return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))
    
    return render_template('admin/bookings/new.html', form=form)

@admin_bookings_bp.route('/<int:booking_id>')
def view_booking(booking_id):
    """View a booking"""
    booking = Booking.query.get_or_404(booking_id)
    return render_template('admin/bookings/view.html', booking=booking)

@admin_bookings_bp.route('/<int:booking_id>/edit', methods=['GET', 'POST'])
def edit_booking(booking_id):
    """Edit a booking"""
    booking = Booking.query.get_or_404(booking_id)
    form = BookingForm(obj=booking)
    
    if form.validate_on_submit():
        form.populate_obj(booking)
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))
    
    return render_template('admin/bookings/edit.html', form=form, booking=booking)

@admin_bookings_bp.route('/<int:booking_id>/delete', methods=['DELETE', 'POST'])
def delete_booking(booking_id):
    """Delete a booking"""
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    
    # Check if HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        flash('Booking deleted successfully.', 'success')
        return redirect(url_for('admin_bookings.list_bookings'))
    
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('admin_bookings.list_bookings'))

@admin_bookings_bp.route('/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    """Confirm a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.confirm()
    
    # Check if HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        flash('Booking confirmed successfully!', 'success')
        return redirect(url_for('admin_bookings.list_bookings'))
    
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))

@admin_bookings_bp.route('/<int:booking_id>/complete', methods=['POST'])
def complete_booking(booking_id):
    """Mark booking as completed"""
    booking = Booking.query.get_or_404(booking_id)
    booking.complete()
    
    # Check if HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        flash('Booking marked as completed!', 'success')
        return redirect(url_for('admin_bookings.list_bookings'))
    
    flash('Booking marked as completed!', 'success')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))

@admin_bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.cancel()
    
    # Check if HTMX request
    is_htmx = request.headers.get('HX-Request') == 'true'
    if is_htmx:
        flash('Booking cancelled.', 'info')
        return redirect(url_for('admin_bookings.list_bookings'))
    
    flash('Booking cancelled.', 'info')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))

# API endpoints for autocomplete
@admin_bookings_bp.route('/api/customers/search')
def search_customers():
    """Search customers for autocomplete"""
    query = request.args.get('q', '')
    customers = Customer.query.filter(
        db.or_(
            Customer.first_name.ilike(f'%{query}%'),
            Customer.last_name.ilike(f'%{query}%'),
            Customer.email.ilike(f'%{query}%'),
            Customer.phone.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return jsonify([{
        'id': c.id,
        'text': f"{c.first_name} {c.last_name} - {c.email} ({c.phone})"
    } for c in customers])

@admin_bookings_bp.route('/api/vehicles/search')
def search_vehicles():
    """Search vehicles for autocomplete"""
    query = request.args.get('q', '')
    vehicles = Vehicle.query.filter(
        db.or_(
            Vehicle.registration_number.ilike(f'%{query}%'),
            Vehicle.make.ilike(f'%{query}%'),
            Vehicle.model.ilike(f'%{query}%'),
            Vehicle.vin.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return jsonify([{
        'id': v.id,
        'text': f"{v.registration_number} - {v.make} {v.model} ({v.year})"
    } for v in vehicles])