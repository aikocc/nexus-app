from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import Booking, Customer, Vehicle, Lead
from forms.admin.booking_forms import BookingForm, BookingSearchForm
from extensions import db
from datetime import datetime, timedelta
import calendar, math

admin_bookings_bp = Blueprint('admin_bookings', __name__, url_prefix='/admin/bookings')

@admin_bookings_bp.route('/')
def list_bookings():
    """List all bookings with filters, pagination, calendar view, and day view"""
    
    # Get all filter parameters from request
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    view = request.args.get('view', 'list')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get calendar/day view parameters
    month = request.args.get('month', datetime.now().month, type=int)
    year = request.args.get('year', datetime.now().year, type=int)
    day = request.args.get('day', datetime.now().day, type=int)
    
    # Validate month/year
    if month < 1 or month > 12:
        month = datetime.now().month
    if year < 2000 or year > 2100:
        year = datetime.now().year
    
    # Create date object for day view
    try:
        day_date = datetime(year, month, day)
    except ValueError:
        day_date = datetime.now()
        day = day_date.day
        month = day_date.month
        year = day_date.year
    
    # ============================================
    # BUILD BASE QUERY WITH FILTERS
    # ============================================
    def apply_filters(query):
        """Apply all filters to a query"""
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
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        if date_from:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(Booking.scheduled_date >= from_date)
            except ValueError:
                pass
        if date_to:
            try:
                to_date = datetime.strptime(date_to, '%Y-%m-%d')
                query = query.filter(Booking.scheduled_date <= to_date)
            except ValueError:
                pass
        return query
    
    # ============================================
    # GET LIST VIEW DATA (Paginated)
    # ============================================
    list_query = Booking.query
    list_query = apply_filters(list_query)
    list_query = list_query.order_by(Booking.created_at.desc())
    pagination = list_query.paginate(page=page, per_page=per_page, error_out=False)
    bookings = pagination.items
    
    # ============================================
    # GET STATS
    # ============================================
    stats = {
        'total': Booking.query.count(),
        'pending': Booking.query.filter_by(status='pending').count(),
        'confirmed': Booking.query.filter_by(status='confirmed').count(),
        'completed': Booking.query.filter_by(status='completed').count()
    }
    
    # ============================================
    # GET CALENDAR DATA
    # ============================================
    month_name = calendar.month_name[month]
    cal = calendar.monthcalendar(year, month)
    
    calendar_days = []
    for week in cal:
        for day_num in week:
            if day_num == 0:
                calendar_days.append({
                    'day': 0,
                    'is_today': False,
                    'is_current_month': False,
                    'booking_count': 0,
                    'bookings': []
                })
            else:
                date_obj = datetime(year, month, day_num)
                is_today = date_obj.date() == datetime.now().date()
                
                # Get bookings for this day with filters applied
                day_query = Booking.query.filter(
                    db.func.date(Booking.scheduled_date) == date_obj.date()
                )
                day_query = apply_filters(day_query)
                day_bookings_list = day_query.all()
                
                calendar_days.append({
                    'day': day_num,
                    'is_today': is_today,
                    'is_current_month': True,
                    'booking_count': len(day_bookings_list),
                    'bookings': day_bookings_list[:5]  # Limit to 5 bookings per day
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
    
    # ============================================
    # GET DAY VIEW DATA - FIXED
    # ============================================
    
    # Method 1: Using db.func.date (works with SQLite, PostgreSQL, MySQL)
    day_query = Booking.query.filter(
        db.func.date(Booking.scheduled_date) == day_date.date()
    )
    day_query = apply_filters(day_query)
    day_query = day_query.order_by(Booking.scheduled_time)
    day_bookings = day_query.all()
    
    # If no results, try Method 2: Using date range (more reliable for SQLite)
    if not day_bookings:
        day_start = datetime(year, month, day, 0, 0, 0)
        day_end = datetime(year, month, day, 23, 59, 59)
        day_query = Booking.query.filter(
            Booking.scheduled_date >= day_start.date(),
            Booking.scheduled_date <= day_end.date()
        )
        day_query = apply_filters(day_query)
        day_query = day_query.order_by(Booking.scheduled_time)
        day_bookings = day_query.all()

    def compute_day_layout(bookings, slot_minutes=30, start_hour=8, end_hour=18):
        total_slots = int((end_hour - start_hour) * 60 / slot_minutes)
        events = []
        day_start_min = start_hour * 60

        for b in bookings:
            if not b.scheduled_time:
                continue
            start_min = b.scheduled_time.hour * 60 + b.scheduled_time.minute
            start_slot = max(0, (start_min - day_start_min) // slot_minutes)
            duration = b.duration_minutes or 60
            span = max(1, math.ceil(duration / slot_minutes))
            end_slot = min(total_slots, start_slot + span)
            if end_slot <= start_slot:
                continue
            events.append({'booking': b, 'start_slot': start_slot, 'span': end_slot - start_slot})

        # assign side-by-side lanes for overlapping bookings
        events.sort(key=lambda e: (e['start_slot'], -e['span']))
        lane_ends = []
        for e in events:
            placed = False
            for lane_idx, lane_end in enumerate(lane_ends):
                if e['start_slot'] >= lane_end:
                    lane_ends[lane_idx] = e['start_slot'] + e['span']
                    e['lane'] = lane_idx
                    placed = True
                    break
            if not placed:
                lane_ends.append(e['start_slot'] + e['span'])
                e['lane'] = len(lane_ends) - 1

        max_lanes = max(len(lane_ends), 1)
        return events, total_slots, max_lanes

    day_events, day_total_slots, day_max_lanes = compute_day_layout(day_bookings)

    day_stats = {
        'total': len(day_bookings),
        'pending': len([b for b in day_bookings if b.status == 'pending']),
        'confirmed': len([b for b in day_bookings if b.status == 'confirmed']),
        'in_progress': len([b for b in day_bookings if b.status == 'in_progress']),
        'completed': len([b for b in day_bookings if b.status == 'completed']),
        'cancelled': len([b for b in day_bookings if b.status == 'cancelled']),
        'no_show': len([b for b in day_bookings if b.status == 'no_show'])
    }
    
    # Previous and next day navigation
    prev_day = day_date - timedelta(days=1)
    next_day = day_date + timedelta(days=1)
    
    # ============================================
    # CHECK IF AJAX REQUEST
    # ============================================
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # ============================================
    # RENDER RESPONSE
    # ============================================
    if is_ajax:
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
            current_year=year,
            day_date=day_date,
            day_bookings=day_bookings,
            day_stats=day_stats,
            prev_day=prev_day,
            next_day=next_day,
            search=search,
            status=status,
            priority=priority,
            date_from=date_from,
            date_to=date_to,
            day_events=day_events,
            day_total_slots=day_total_slots,
            day_max_lanes=day_max_lanes
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
            current_year=year,
            day_date=day_date,
            day_bookings=day_bookings,
            day_stats=day_stats,
            prev_day=prev_day,
            next_day=next_day,
            search=search,
            status=status,
            priority=priority,
            date_from=date_from,
            date_to=date_to,
            day_events=day_events,
            day_total_slots=day_total_slots,
            day_max_lanes=day_max_lanes
        )

@admin_bookings_bp.route('/new', methods=['GET', 'POST'])
def new_booking():
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
            form.service_type.data = 'engine_scan'
    
    if form.validate_on_submit():
        booking = Booking()
        form.populate_obj(booking)
        
        # Generate booking number
        booking.booking_number = booking.generate_booking_number()
        
        # Try to link to existing customer
        customer = None
        if form.customer_search.data:
            try:
                customer_id = int(form.customer_search.data)
                customer = Customer.query.get(customer_id)
            except (ValueError, TypeError):
                pass
        else:
            if form.customer_email.data:
                customer = Customer.query.filter_by(email=form.customer_email.data).first()
        
        if customer:
            booking.link_to_customer(customer)
        else:
            # Create new customer if email exists
            if form.customer_email.data:
                # Check if customer already exists
                existing = Customer.query.filter_by(email=form.customer_email.data).first()
                if existing:
                    booking.link_to_customer(existing)
        
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
    """View a single booking with combined view/edit functionality"""
    booking = Booking.query.get_or_404(booking_id)
    
    # Get related data
    customer = booking.customer
    vehicle = booking.vehicle
    lead = booking.lead
    
    # Get booking history (previous bookings for same customer)
    previous_bookings = []
    if customer:
        previous_bookings = Booking.query.filter(
            Booking.customer_id == customer.id,
            Booking.id != booking_id
        ).order_by(Booking.scheduled_date.desc()).limit(5).all()
    
    # If no customer linked but we have email, try to find previous bookings
    elif booking.customer_email:
        previous_bookings = Booking.query.filter(
            Booking.customer_email == booking.customer_email,
            Booking.id != booking_id
        ).order_by(Booking.scheduled_date.desc()).limit(5).all()
    
    # Create form instance for the combined view/edit page
    form = BookingForm(obj=booking)
    
    return render_template(
        'admin/bookings/view.html',
        booking=booking,
        customer=customer,
        vehicle=vehicle,
        lead=lead,
        previous_bookings=previous_bookings,
        form=form
    )

@admin_bookings_bp.route('/<int:booking_id>/update', methods=['POST'])
def update_booking(booking_id):
    """Update a booking from the combined view/edit page"""
    booking = Booking.query.get_or_404(booking_id)
    form = BookingForm(obj=booking)
    
    if form.validate_on_submit():
        form.populate_obj(booking)
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Booking updated successfully!', 'success')
        return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))
    
    # If validation fails, re-render with errors
    customer = booking.customer
    vehicle = booking.vehicle
    lead = booking.lead
    
    previous_bookings = []
    if customer:
        previous_bookings = Booking.query.filter(
            Booking.customer_id == customer.id,
            Booking.id != booking_id
        ).order_by(Booking.scheduled_date.desc()).limit(5).all()
    elif booking.customer_email:
        previous_bookings = Booking.query.filter(
            Booking.customer_email == booking.customer_email,
            Booking.id != booking_id
        ).order_by(Booking.scheduled_date.desc()).limit(5).all()
    
    return render_template(
        'admin/bookings/view.html',
        booking=booking,
        customer=customer,
        vehicle=vehicle,
        lead=lead,
        previous_bookings=previous_bookings,
        form=form
    )


@admin_bookings_bp.route('/<int:booking_id>/delete', methods=['DELETE', 'POST'])
def delete_booking(booking_id):
    """Delete a booking"""
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    
    flash('Booking deleted successfully.', 'success')
    return redirect(url_for('admin_bookings.list_bookings'))


@admin_bookings_bp.route('/<int:booking_id>/confirm', methods=['POST'])
def confirm_booking(booking_id):
    """Confirm a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.confirm()
    
    flash('Booking confirmed successfully!', 'success')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))


@admin_bookings_bp.route('/<int:booking_id>/complete', methods=['POST'])
def complete_booking(booking_id):
    """Mark booking as completed"""
    booking = Booking.query.get_or_404(booking_id)
    booking.complete()
    
    flash('Booking marked as completed!', 'success')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))


@admin_bookings_bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    booking = Booking.query.get_or_404(booking_id)
    booking.cancel()
    
    flash('Booking cancelled.', 'info')
    return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))


# ============================================
# API ENDPOINTS FOR AUTOCOMPLETE
# ============================================

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