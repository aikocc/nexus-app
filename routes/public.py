from database import db, Lead

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for # pyright: ignore[reportMissingImports]

public_bp = Blueprint("public", __name__, url_prefix="")


@public_bp.route('/')
def index():
    return render_template('index.html')


@public_bp.route('/book', methods=['POST'])
def book():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    required = ['name', 'phone', 'email', 'vehicle', 'service', 'rego', 'rego-state', 'address', 'urgency']
    missing  = [f for f in required if not data.get(f, '').strip()]
    if missing:
        msg = f"Missing fields: {', '.join(missing)}"
        if request.is_json:
            return jsonify({'ok': False, 'error': msg}), 400
        flash(msg, 'error')
        return redirect(url_for('index') + '#booking')

    lead = Lead(
        name=data['name'].strip(),
        phone=data['phone'].strip(),
        email=data['email'].strip(),
        vehicle=data['vehicle'].strip(),
        service=data['service'].strip(),
        rego=data['rego'].strip(),
        rego_state=data['rego-state'].strip(),
        address=data['address'].strip(),
        urgency=data['urgency'].strip(),
        notes=data.get('notes', '').strip(),
    )
    db.session.add(lead)
    db.session.commit()

    if request.is_json:
        return jsonify({'ok': True, 'id': lead.id})
    return render_template('confirmation.html', booking=lead)
