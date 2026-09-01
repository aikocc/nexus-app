from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Vehicle, Customer
from forms.admin.vehicle_forms import VehicleForm

admin_vehicles_bp = Blueprint('admin_vehicles', __name__, url_prefix='/admin/vehicles')


@admin_vehicles_bp.route('/')
def list_vehicles():
    vehicles = Vehicle.query.all()
    return render_template('admin/vehicles/list.html', vehicles=vehicles)


@admin_vehicles_bp.route('/new', methods=['GET', 'POST'])
def create_vehicle():
    form = VehicleForm()
    
    if form.validate_on_submit():
        customer = Customer.query.get(form.customer_id.data)
        if not customer:
            flash('Please select a valid customer.', 'error')
            return render_template('admin/vehicles/edit.html', form=form, title='New Vehicle')
        
        vehicle = Vehicle(
            customer_id=form.customer_id.data,
            registration_no=form.registration_no.data,
            rego_state=form.rego_state.data if hasattr(form, 'rego_state') else None,
            vin=form.vin.data,
            make=form.make.data,
            model=form.model.data,
            sub_model=form.sub_model.data if hasattr(form, 'sub_model') else None,
            series=form.series.data if hasattr(form, 'series') else None,
            year=form.year.data,
            body_type=form.body_type.data if hasattr(form, 'body_type') and form.body_type.data else None,
            drive_type=form.drive_type.data if hasattr(form, 'drive_type') and form.drive_type.data else None,
            fuel_type=form.fuel_type.data if form.fuel_type.data else None,
            transmission=form.transmission.data if form.transmission.data else None,
            engine_spec=form.engine_spec.data if hasattr(form, 'engine_spec') else None,
            chassis_no=form.chassis_no.data if hasattr(form, 'chassis_no') else None,
            color=form.color.data if hasattr(form, 'color') else None,
            odometer_reading=form.odometer_reading.data if hasattr(form, 'odometer_reading') else None,
            notes=form.notes.data
        )
        db.session.add(vehicle)
        db.session.commit()
        flash('Vehicle created successfully!', 'success')
        return redirect(url_for('admin_vehicles.list_vehicles'))
    
    return render_template('admin/vehicles/edit.html', form=form, title='New Vehicle')


@admin_vehicles_bp.route('/<int:vehicle_id>/edit', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    form = VehicleForm(obj=vehicle)
    
    if request.method == 'GET' and vehicle.customer:
        form.customer_search.data = vehicle.customer.full_name
    
    if form.validate_on_submit():
        customer = Customer.query.get(form.customer_id.data)
        if not customer:
            flash('Please select a valid customer.', 'error')
            return render_template('admin/vehicle_form.html', form=form, title='Edit Vehicle', vehicle=vehicle)
        
        vehicle.customer_id = form.customer_id.data
        vehicle.registration_no = form.registration_no.data
        vehicle.vin = form.vin.data
        vehicle.make = form.make.data
        vehicle.model = form.model.data
        vehicle.year = form.year.data
        vehicle.fuel_type = form.fuel_type.data if form.fuel_type.data else None
        vehicle.transmission = form.transmission.data if form.transmission.data else None
        vehicle.color = form.color.data if hasattr(form, 'color') else None
        vehicle.odometer_reading = form.odometer_reading.data if hasattr(form, 'odometer_reading') else None
        vehicle.notes = form.notes.data
        
        # Update additional fields if they exist on form
        if hasattr(form, 'rego_state'):
            vehicle.rego_state = form.rego_state.data
        if hasattr(form, 'sub_model'):
            vehicle.sub_model = form.sub_model.data
        if hasattr(form, 'series'):
            vehicle.series = form.series.data
        if hasattr(form, 'body_type') and form.body_type.data:
            vehicle.body_type = form.body_type.data
        if hasattr(form, 'drive_type') and form.drive_type.data:
            vehicle.drive_type = form.drive_type.data
        if hasattr(form, 'engine_spec'):
            vehicle.engine_spec = form.engine_spec.data
        if hasattr(form, 'chassis_no'):
            vehicle.chassis_no = form.chassis_no.data
        
        db.session.commit()
        flash('Vehicle updated successfully!', 'success')
        return redirect(url_for('admin_vehicles.list_vehicles'))
    
    return render_template('admin/vehicles/edit.html', form=form, title='Edit Vehicle', vehicle=vehicle)


@admin_vehicles_bp.route('/<int:vehicle_id>/delete', methods=['POST'])
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    registration = vehicle.registration_no
    
    db.session.delete(vehicle)
    db.session.commit()
    
    flash(f'Vehicle {registration} deleted successfully!', 'success')
    return redirect(url_for('admin_vehicles.list_vehicles'))