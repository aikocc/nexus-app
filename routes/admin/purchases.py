# from database import db, PurchaseInvoice, Supplier, PURCHASE_CATEGORIES
# from decorators import login_required

# from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for  # pyright: ignore[reportMissingImports]
# import datetime

# purchases_bp = Blueprint("purchases", __name__, url_prefix="/admin/purchases")

# @purchases_bp.route('/admin/purchases')
# @login_required
# def admin_purchases():
#     status_filter = request.args.get('status', 'all')
#     query = PurchaseInvoice.query.order_by(PurchaseInvoice.invoice_date.desc())
#     if status_filter != 'all':
#         query = query.filter_by(status=status_filter)
#     purchases = query.all()

#     counts = {
#         'all':     PurchaseInvoice.query.count(),
#         'unpaid':  PurchaseInvoice.query.filter_by(status='unpaid').count(),
#         'paid':    PurchaseInvoice.query.filter_by(status='paid').count(),
#         'overdue': PurchaseInvoice.query.filter_by(status='overdue').count(),
#     }
#     spend = {
#         'paid':        db.session.query(db.func.sum(PurchaseInvoice.total)).filter_by(status='paid').scalar() or 0,
#         'outstanding': db.session.query(db.func.sum(PurchaseInvoice.total)).filter(
#                            PurchaseInvoice.status.in_(['unpaid', 'overdue'])).scalar() or 0,
#     }
#     suppliers = Supplier.query.order_by(Supplier.name).all()
#     return render_template('admin_purchases.html', purchases=purchases,
#                            counts=counts, spend=spend,
#                            active_filter=status_filter, suppliers=suppliers)


# @purchases_bp.route('/admin/purchases/new', methods=['GET', 'POST'])
# @login_required
# def admin_purchase_new():
#     suppliers = Supplier.query.order_by(Supplier.name).all()
#     if request.method == 'POST':
#         descs = request.form.getlist('item_desc[]')
#         qtys  = request.form.getlist('item_qty[]')
#         units = request.form.getlist('item_unit[]')
#         items = [{'desc': d.strip(), 'qty': float(q or 1), 'unit': float(u or 0)}
#                  for d, q, u in zip(descs, qtys, units) if d.strip()]

#         inv_date = request.form.get('invoice_date', '').strip()
#         due_date = request.form.get('due_date', '').strip()

#         p = PurchaseInvoice(
#             supplier_id  = int(request.form['supplier_id']),
#             supplier_ref = request.form.get('supplier_ref', '').strip(),
#             invoice_date = datetime.strptime(inv_date, '%Y-%m-%d').date() if inv_date else datetime.date.today(),
#             due_date     = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None,
#             category     = request.form.get('category', '').strip(),
#             tax_rate     = float(request.form.get('tax_rate', 10)),
#             status       = request.form.get('status', 'unpaid'),
#             notes        = request.form.get('notes', '').strip(),
#         )
#         p.recalculate(items)
#         db.session.add(p)
#         db.session.commit()
#         flash(f'Purchase invoice {p.reference} logged.', 'success')
#         return redirect(url_for('admin_purchase_detail', purchase_id=p.id))

#     prefill_supplier_id = request.args.get('supplier_id')
#     return render_template('admin_purchase_form.html', purchase=None,
#                            suppliers=suppliers, prefill_supplier_id=prefill_supplier_id,
#                            categories=PURCHASE_CATEGORIES)


# @purchases_bp.route('/admin/purchases/<int:purchase_id>')
# @login_required
# def admin_purchase_detail(purchase_id):
#     purchase = PurchaseInvoice.query.get_or_404(purchase_id)
#     return render_template('admin_purchase_detail.html', purchase=purchase)


# @purchases_bp.route('/admin/purchases/<int:purchase_id>/edit', methods=['GET', 'POST'])
# @login_required
# def admin_purchase_edit(purchase_id):
#     purchase  = PurchaseInvoice.query.get_or_404(purchase_id)
#     suppliers = Supplier.query.order_by(Supplier.name).all()
#     if request.method == 'POST':
#         descs = request.form.getlist('item_desc[]')
#         qtys  = request.form.getlist('item_qty[]')
#         units = request.form.getlist('item_unit[]')
#         items = [{'desc': d.strip(), 'qty': float(q or 1), 'unit': float(u or 0)}
#                  for d, q, u in zip(descs, qtys, units) if d.strip()]

#         inv_date = request.form.get('invoice_date', '').strip()
#         due_date = request.form.get('due_date', '').strip()

#         purchase.supplier_id  = int(request.form['supplier_id'])
#         purchase.supplier_ref = request.form.get('supplier_ref', '').strip()
#         purchase.invoice_date = datetime.strptime(inv_date, '%Y-%m-%d').date() if inv_date else purchase.invoice_date
#         purchase.due_date     = datetime.strptime(due_date, '%Y-%m-%d').date() if due_date else None
#         purchase.category     = request.form.get('category', '').strip()
#         purchase.tax_rate     = float(request.form.get('tax_rate', 10))
#         purchase.status       = request.form.get('status', purchase.status)
#         purchase.notes        = request.form.get('notes', '').strip()
#         purchase.recalculate(items)
#         db.session.commit()
#         flash(f'Purchase invoice {purchase.reference} updated.', 'success')
#         return redirect(url_for('admin_purchase_detail', purchase_id=purchase.id))

#     return render_template('admin_purchase_form.html', purchase=purchase,
#                            suppliers=suppliers, prefill_supplier_id=None,
#                            categories=PURCHASE_CATEGORIES)


# @purchases_bp.route('/admin/purchases/<int:purchase_id>/status', methods=['POST'])
# @login_required
# def admin_purchase_status(purchase_id):
#     purchase   = PurchaseInvoice.query.get_or_404(purchase_id)
#     new_status = request.form.get('status')
#     if new_status in {'unpaid', 'paid', 'overdue'}:
#         purchase.status = new_status
#         if new_status == 'paid':
#             purchase.paid_date = datetime.date.today()
#         db.session.commit()
#         flash(f'{purchase.reference} marked as {new_status}.', 'success')
#     return redirect(url_for('admin_purchase_detail', purchase_id=purchase_id))


# @purchases_bp.route('/admin/purchases/<int:purchase_id>/delete', methods=['POST'])
# @login_required
# def admin_purchase_delete(purchase_id):
#     purchase = PurchaseInvoice.query.get_or_404(purchase_id)
#     db.session.delete(purchase)
#     db.session.commit()
#     flash('Purchase invoice deleted.', 'success')
#     return redirect(url_for('admin_purchases'))


# @purchases_bp.route('/admin/api/purchases')
# @login_required
# def admin_api_purchases():
#     purchases = PurchaseInvoice.query.order_by(PurchaseInvoice.invoice_date.desc()).all()
#     return jsonify([p.to_dict() for p in purchases])