from flask import Blueprint, render_template

admin_invoices_bp = Blueprint('admin_invoices', __name__, url_prefix='/admin/invoices')


@admin_invoices_bp.route('/')
def list_invoices():
    """List all invoices"""
    return render_template('admin/invoice_create.html')