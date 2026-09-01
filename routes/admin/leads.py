from flask import Blueprint, render_template, redirect, url_for, flash
import datetime

from extensions import db
from models import Lead, Customer, Vehicle, Booking
from forms.admin.lead_forms import LeadForm
admin_leads_bp = Blueprint('admin_leads', __name__, url_prefix='/admin/leads')


@admin_leads_bp.route('/')
def list_leads():
    leads = Lead.query.all()
    leads.sort(key=lambda x: x.created_at, reverse=True)  # Sort by created_at in descending order
    return render_template('admin/leads/list.html', leads=leads)


@admin_leads_bp.route('/<int:lead_id>', methods=['GET', 'POST'])
def view_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    form = LeadForm(obj=lead)

    if form.validate_on_submit():
        # Update lead with form data
        form.populate_obj(lead)
        lead.converted = True
        lead.converted_at = datetime.utcnow()
        db.session.commit()
        
        # Create booking from lead
        booking = Booking()
        booking.sync_from_lead(lead)
        
        # Try to link to existing customer
        customer = Customer.query.filter_by(email=lead.email).first()
        if customer:
            booking.link_to_customer(customer)
        
        # Try to link to existing vehicle
        vehicle = Vehicle.query.filter_by(registration_number=lead.rego).first()
        if vehicle:
            booking.link_to_vehicle(vehicle)
        
        # Set defaults
        booking.service_type = 'engine_scan'  # Or let admin choose
        booking.status = 'pending'
        booking.priority = 'normal'
        
        db.session.add(booking)
        db.session.commit()
        
        lead.booking_id = booking.id
        db.session.commit()
        
        flash('Lead converted to booking successfully!', 'success')
        return redirect(url_for('admin_bookings.view_booking', booking_id=booking.id))

    return render_template('admin/leads/view.html', lead=lead, form=form)


@admin_leads_bp.route('/<int:lead_id>/delete', methods=['POST'])
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    
    lead.active = False  # Mark the lead as inactive instead of deleting
    db.session.commit()
    
    flash(f'Lead {lead} deleted successfully!', 'success')
    return redirect(url_for('admin_leads.list_leads'))