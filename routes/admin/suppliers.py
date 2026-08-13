# from database import db, Supplier
# from decorators import login_required

# from flask import Blueprint, request, render_template, flash, redirect, url_for # pyright: ignore[reportMissingImports]

# suppliers_bp = Blueprint("suppliers", __name__, url_prefix="/admin/suppliers")

# @suppliers_bp.route('/admin/suppliers')
# @login_required
# def admin_suppliers():
#     suppliers = Supplier.query.order_by(Supplier.name).all()
#     return render_template('admin_suppliers.html', suppliers=suppliers)


# @suppliers_bp.route('/admin/suppliers/new', methods=['GET', 'POST'])
# @login_required
# def admin_supplier_new():
#     if request.method == 'POST':
#         s = Supplier(
#             name          = request.form['name'].strip(),
#             contact_name  = request.form.get('contact_name', '').strip(),
#             email         = request.form.get('email', '').strip(),
#             phone         = request.form.get('phone', '').strip(),
#             abn           = request.form.get('abn', '').strip(),
#             address       = request.form.get('address', '').strip(),
#             payment_terms = int(request.form.get('payment_terms', 30)),
#             notes         = request.form.get('notes', '').strip(),
#         )
#         db.session.add(s)
#         db.session.commit()
#         flash(f'Supplier "{s.name}" added.', 'success')
#         return redirect(url_for('admin_suppliers'))
#     return render_template('admin_supplier_form.html', supplier=None)


# @suppliers_bp.route('/admin/suppliers/<int:supplier_id>/edit', methods=['GET', 'POST'])
# @login_required
# def admin_supplier_edit(supplier_id):
#     s = Supplier.query.get_or_404(supplier_id)
#     if request.method == 'POST':
#         s.name          = request.form['name'].strip()
#         s.contact_name  = request.form.get('contact_name', '').strip()
#         s.email         = request.form.get('email', '').strip()
#         s.phone         = request.form.get('phone', '').strip()
#         s.abn           = request.form.get('abn', '').strip()
#         s.address       = request.form.get('address', '').strip()
#         s.payment_terms = int(request.form.get('payment_terms', 30))
#         s.notes         = request.form.get('notes', '').strip()
#         db.session.commit()
#         flash(f'Supplier "{s.name}" updated.', 'success')
#         return redirect(url_for('admin_suppliers'))
#     return render_template('admin_supplier_form.html', supplier=s)


# @suppliers_bp.route('/admin/suppliers/<int:supplier_id>/delete', methods=['POST'])
# @login_required
# def admin_supplier_delete(supplier_id):
#     s = Supplier.query.get_or_404(supplier_id)
#     if s.purchases:
#         flash('Cannot delete supplier with existing purchase invoices.', 'error')
#         return redirect(url_for('admin_suppliers'))
#     db.session.delete(s)
#     db.session.commit()
#     flash('Supplier deleted.', 'success')
#     return redirect(url_for('admin_suppliers'))