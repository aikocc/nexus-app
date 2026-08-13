# from database import db, Invoice, Booking
# from decorators import login_required

# from flask import Blueprint, request, render_template, flash, redirect, url_for, jsonify # pyright: ignore[reportMissingImports]
# import datetime

# invoices_bp = Blueprint("invoices", __name__, url_prefix="/admin/invoices")

# @invoices_bp.route('/admin/invoices')
# @login_required
# def admin_invoices():
#     status_filter = request.args.get('status', 'all')
#     query = Invoice.query.order_by(Invoice.created_at.desc())
#     if status_filter != 'all':
#         query = query.filter_by(status=status_filter)
#     invoices = query.all()

#     counts = {
#         'all':       Invoice.query.count(),
#         'draft':     Invoice.query.filter_by(status='draft').count(),
#         'sent':      Invoice.query.filter_by(status='sent').count(),
#         'paid':      Invoice.query.filter_by(status='paid').count(),
#         'overdue':   Invoice.query.filter_by(status='overdue').count(),
#         'cancelled': Invoice.query.filter_by(status='cancelled').count(),
#     }
#     revenue = {
#         'paid':    db.session.query(db.func.sum(Invoice.total)).filter_by(status='paid').scalar() or 0,
#         'outstanding': db.session.query(db.func.sum(Invoice.total)).filter(
#             Invoice.status.in_(['sent', 'overdue'])).scalar() or 0,
#     }
#     return render_template('admin_invoices.html', invoices=invoices,
#                            counts=counts, revenue=revenue, active_filter=status_filter)


# @invoices_bp.route('/admin/invoices/new', methods=['GET', 'POST'])
# @login_required
# def admin_invoice_new():
#     bookings = Booking.query.order_by(Booking.created_at.desc()).all()

#     if request.method == 'POST':
#         # Parse line items from the dynamic form fields
#         descs  = request.form.getlist('item_desc[]')
#         qtys   = request.form.getlist('item_qty[]')
#         units  = request.form.getlist('item_unit[]')
#         notes_ = request.form.getlist('item_note[]')
#         items  = []
#         for i, (d, q, u) in enumerate(zip(descs, qtys, units)):
#             if d.strip():
#                 note = notes_[i].strip() if i < len(notes_) else ''
#                 items.append({'desc': d.strip(),
#                               'qty': float(q or 1),
#                               'unit': float(u or 0),
#                               'note': note})

#         due_str = request.form.get('due_date', '').strip()
#         due_date = datetime.strptime(due_str, '%Y-%m-%d').date() if due_str else None

#         booking_id = request.form.get('booking_id') or None
#         booking_id = int(booking_id) if booking_id else None

#         inv = Invoice(
#             booking_id       = booking_id,
#             customer_name    = request.form['customer_name'].strip(),
#             customer_email   = request.form['customer_email'].strip(),
#             customer_phone   = request.form.get('customer_phone', '').strip(),
#             customer_address = request.form.get('customer_address', '').strip(),
#             vehicle          = request.form.get('vehicle', '').strip(),
#             tax_rate         = float(request.form.get('tax_rate', 10)),
#             status           = request.form.get('status', 'draft'),
#             notes            = request.form.get('notes', '').strip(),
#             due_date         = due_date,
#         )
#         inv.recalculate(items)
#         db.session.add(inv)
#         db.session.commit()
#         flash(f'Invoice {inv.invoice_number} created.', 'success')
#         return redirect(url_for('admin_invoice_detail', invoice_id=inv.id))

#     # Pre-fill from a booking if ?booking_id= passed
#     prefill_booking = None
#     bid = request.args.get('booking_id')
#     if bid:
#         prefill_booking = Booking.query.get(int(bid))

#     return render_template('admin_invoice_form.html', invoice=None,
#                            bookings=bookings, prefill_booking=prefill_booking)
 

# @invoices_bp.route('/admin/invoices/<int:invoice_id>')
# @login_required
# def admin_invoice_detail(invoice_id):
#     invoice = Invoice.query.get_or_404(invoice_id)
#     return render_template('admin_invoice_detail.html', invoice=invoice)


# @invoices_bp.route('/admin/invoices/<int:invoice_id>/edit', methods=['GET', 'POST'])
# @login_required
# def admin_invoice_edit(invoice_id):
#     invoice  = Invoice.query.get_or_404(invoice_id)
#     bookings = Booking.query.order_by(Booking.created_at.desc()).all()

#     if request.method == 'POST':
#         descs = request.form.getlist('item_desc[]')
#         qtys  = request.form.getlist('item_qty[]')
#         units = request.form.getlist('item_unit[]')
#         notes_ = request.form.getlist('item_note[]')
#         items = []
#         for i, (d, q, u) in enumerate(zip(descs, qtys, units)):
#             if d.strip():
#                 note = notes_[i].strip() if i < len(notes_) else ''
#                 items.append({'desc': d.strip(),
#                               'qty': float(q or 1),
#                               'unit': float(u or 0),
#                               'note': note})

#         due_str  = request.form.get('due_date', '').strip()
#         due_date = datetime.strptime(due_str, '%Y-%m-%d').date() if due_str else None

#         bid = request.form.get('booking_id') or None
#         invoice.booking_id       = int(bid) if bid else None
#         invoice.customer_name    = request.form['customer_name'].strip()
#         invoice.customer_email   = request.form['customer_email'].strip()
#         invoice.customer_phone   = request.form.get('customer_phone', '').strip()
#         invoice.customer_address = request.form.get('customer_address', '').strip()
#         invoice.vehicle          = request.form.get('vehicle', '').strip()
#         invoice.tax_rate         = float(request.form.get('tax_rate', 10))
#         invoice.status           = request.form.get('status', invoice.status)
#         invoice.notes            = request.form.get('notes', '').strip()
#         invoice.due_date         = due_date
#         invoice.recalculate(items)
#         db.session.commit()
#         flash(f'Invoice {invoice.invoice_number} updated.', 'success')
#         return redirect(url_for('admin_invoice_detail', invoice_id=invoice.id))

#     return render_template('admin_invoice_form.html', invoice=invoice,
#                            bookings=bookings, prefill_booking=None)


# @invoices_bp.route('/admin/invoices/<int:invoice_id>/status', methods=['POST'])
# @login_required
# def admin_invoice_status(invoice_id):
#     invoice    = Invoice.query.get_or_404(invoice_id)
#     new_status = request.form.get('status')
#     valid      = {'draft', 'sent', 'paid', 'overdue', 'cancelled'}
#     if new_status in valid:
#         invoice.status = new_status
#         db.session.commit()
#         flash(f'{invoice.invoice_number} marked as {new_status}.', 'success')
#     return redirect(url_for('admin_invoice_detail', invoice_id=invoice_id))


# @invoices_bp.route('/admin/invoices/<int:invoice_id>/delete', methods=['POST'])
# @login_required
# def admin_invoice_delete(invoice_id):
#     invoice = Invoice.query.get_or_404(invoice_id)
#     db.session.delete(invoice)
#     db.session.commit()
#     flash('Invoice deleted.', 'success')
#     return redirect(url_for('admin_invoices'))


# @invoices_bp.route('/admin/invoices/<int:invoice_id>/print')
# @login_required
# def admin_invoice_print(invoice_id):
#     invoice = Invoice.query.get_or_404(invoice_id)
#     return render_template('invoice_print.html', invoice=invoice)


# @invoices_bp.route('/admin/api/invoices')
# @login_required
# def admin_api_invoices():
#     invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
#     return jsonify([i.to_dict() for i in invoices])
