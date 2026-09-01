from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Customer
from forms.admin.customer_forms import CustomerForm  # Changed from forms.customer.customer_forms

admin_customers_bp = Blueprint('admin_customers', __name__, url_prefix='/admin/customers')


@admin_customers_bp.route('/')
def list_customers():
    search = request.args.get('search', '')
    
    if search:
        customers = Customer.query.filter(
            db.or_(
                Customer.first_name.ilike(f'%{search}%'),
                Customer.last_name.ilike(f'%{search}%'),
                Customer.email.ilike(f'%{search}%')
            )
        ).all()
    else:
        customers = Customer.query.all()
    
    return render_template('admin/customers/list.html', customers=customers, search=search)


@admin_customers_bp.route('/new', methods=['GET', 'POST'])
def create_customer():
    form = CustomerForm()
    
    if form.validate_on_submit():
        customer = Customer(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            company_name=form.company_name.data,
            email=form.email.data,
            phone=form.phone.data,
            mobile=form.mobile.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            postal_code=form.postal_code.data,
            country=form.country.data,
            tax_id=form.tax_id.data,
            is_company=form.is_company.data,
            notes=form.notes.data
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer created successfully!', 'success')
        return redirect(url_for('admin_customers.list_customers'))
    
    return render_template('admin/customers/edit.html', form=form, title='New Customer')


@admin_customers_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = CustomerForm(obj=customer)
    
    if form.validate_on_submit():
        customer.first_name = form.first_name.data
        customer.last_name = form.last_name.data
        customer.company_name = form.company_name.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        customer.mobile = form.mobile.data
        customer.address = form.address.data
        customer.city = form.city.data
        customer.state = form.state.data
        customer.postal_code = form.postal_code.data
        customer.country = form.country.data
        customer.tax_id = form.tax_id.data
        customer.is_company = form.is_company.data
        customer.notes = form.notes.data
        
        db.session.commit()
        flash('Customer updated successfully!', 'success')
        return redirect(url_for('admin_customers.list_customers'))
    
    return render_template('admin/customers/edit.html', form=form, title='Edit Customer', customer=customer)


@admin_customers_bp.route('/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    name = customer.full_name
    
    db.session.delete(customer)
    db.session.commit()
    
    flash(f'Customer {name} deleted successfully!', 'success')
    return redirect(url_for('admin_customers.list_customers'))