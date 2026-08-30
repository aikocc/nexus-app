from flask import Blueprint, render_template, redirect, url_for, flash
from extensions import db
from models import Leads
from forms.admin.lead_forms import LeadForm
admin_leads_bp = Blueprint('admin_leads', __name__, url_prefix='/admin/leads')


@admin_leads_bp.route('/')
def list_leads():
    leads = Leads.query.all()
    leads.sort(key=lambda x: x.created_at, reverse=True)  # Sort by created_at in descending order
    return render_template('admin/leads_list.html', leads=leads)


@admin_leads_bp.route('/<int:lead_id>', methods=['GET'])
def view_lead(lead_id):
    lead = Leads.query.get_or_404(lead_id)
    form = LeadForm(obj=lead)
    return render_template('admin/leads_view.html', form=form, title='Edit Lead', lead=lead)


@admin_leads_bp.route('/<int:lead_id>/delete', methods=['POST'])
def delete_lead(lead_id):
    lead = Leads.query.get_or_404(lead_id)
    
    lead.active = False  # Mark the lead as inactive instead of deleting
    db.session.commit()
    
    flash(f'Lead {lead} deleted successfully!', 'success')
    return redirect(url_for('admin_leads.list_leads'))