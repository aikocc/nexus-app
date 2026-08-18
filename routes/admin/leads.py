from database import Customer, Vehicle, db, Booking, Lead
from decorators import login_required

from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify  # pyright: ignore[reportMissingImports]

lead_bp = Blueprint("lead", __name__, url_prefix="/admin/lead", template_folder='templates')


@lead_bp.route('/<int:lead_id>')
@login_required
def info(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    if not lead.active:
        flash(f'Lead #{lead_id} is inactive.', 'error')
        return redirect(url_for('admin_dashboard.admin_dashboard'))
    return render_template('admin_lead_detail.html', lead=lead)

@lead_bp.route('/<int:lead_id>/delete', methods=['POST'])
@login_required
def delete(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    lead.active = False
    db.session.commit()
    flash(f'Lead #{lead_id} deleted.', 'success')
    return redirect(url_for('admin_dashboard.admin_dashboard'))