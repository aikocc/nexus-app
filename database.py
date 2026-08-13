from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
from datetime import datetime, timezone, date
from json import loads, dumps

db = SQLAlchemy()

class CustomerVehicle(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    vehicle_id  = db.Column(db.Integer, db.ForeignKey("vehicle.id"))

class Customer(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    first_name  = db.Column(db.String(120), nullable=False)
    last_name   = db.Column(db.String(120), nullable=False)
    phone       = db.Column(db.String(30), nullable=False)
    email       = db.Column(db.String(120), nullable=False)
    street      = db.Column(db.String(200), nullable=False)
    suburb      = db.Column(db.String(26), nullable=False)
    state       = db.Column(db.String(10), nullable=False)
    postcode    = db.Column(db.Integer, nullable=False)
    vehicles    = db.relationship("Vehicle", secondary=CustomerVehicle.__table__, back_populates="owners")
    

class Vehicle(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    make        = db.Column(db.String(30), nullable=False)
    model       = db.Column(db.String(30), nullable=False)
    series      = db.Column(db.String(30), default="")
    year        = db.Column(db.Integer())
    rego        = db.Column(db.String(10), default="No Plate")
    rego_state  = db.Column(db.String(4), default="")
    vin         = db.Column(db.String(17), default="")
    owners      = db.relationship("Customer", secondary=CustomerVehicle.__table__, back_populates="vehicles")

class Lead(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    name        = db.Column(db.String(120), nullable=False)
    phone       = db.Column(db.String(30), nullable=False)
    email       = db.Column(db.String(120), nullable=False)
    address     = db.Column(db.String(200), nullable=False)
    vehicle     = db.Column(db.String(120), nullable=False)
    rego        = db.Column(db.String(120), nullable=False)
    rego_state  = db.Column(db.String(120), nullable=False)
    service     = db.Column(db.String(60), nullable=False)
    urgency     = db.Column(db.String(30), nullable=False)
    notes       = db.Column(db.Text, default="")
    status      = db.Column(db.String(30), default="pending")

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%d %b %Y, %H:%M"),
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "vehicle": self.vehicle,
            "service": self.service,
            "rego": self.rego,
            "rego_state": self.rego_state,
            "address": self.address,
            "urgency": self.urgency,
            "notes": self.notes,
            "status": self.status,
        }

class Booking(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    booking_time= db.Column(db.DateTime, nullable=False)
    vehicle     = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    customer    = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    service     = db.Column(db.String(60), nullable=False)
    urgency     = db.Column(db.String(30), nullable=False)
    notes       = db.Column(db.Text, default="")
    status      = db.Column(db.String(30), default="pending")
    invoices    = db.relationship("Invoice", backref="booking", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": self.created_at.strftime("%d %b %Y, %H:%M"),
            "booking_time": self.booking_time,
            "customer": self.customer,
            "vehicle": self.vehicle,
            "service": self.service,
            "urgency": self.urgency,
            "notes": self.notes,
            "status": self.status,
        }

class Invoice(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    created_at  = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    due_date    = db.Column(db.Date, nullable=True)
    booking_id  = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=True)

    
    vehicle     = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)
    customer    = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)

    # Line items stored as JSON string: [{"desc": "...", "qty": 1, "unit": 120.00}]
    line_items_json  = db.Column(db.Text, default="[]")

    # Financials (computed on save for fast querying)
    subtotal    = db.Column(db.Float, default=0.0)
    tax_rate    = db.Column(db.Float, default=10.0)   # GST % 
    tax_amount  = db.Column(db.Float, default=0.0)
    total       = db.Column(db.Float, default=0.0)

    status      = db.Column(db.String(20), default="draft")  # draft | sent | paid | overdue | cancelled
    notes       = db.Column(db.Text, default="")

    @property
    def invoice_number(self):
        return f"INV-{self.id:04d}"

    @property
    def line_items(self):
        try:
            return loads(self.line_items_json or "[]")
        except Exception:
            return []
 
    def recalculate(self, items):
        """Recalculate totals from list of dicts with qty and unit keys."""
        self.line_items_json = dumps(items)
        self.subtotal  = sum(float(i.get("qty", 1)) * float(i.get("unit", 0)) for i in items)
        rate = float(self.tax_rate) if self.tax_rate is not None else 10.0
        self.tax_amount = round(self.subtotal * (rate / 100), 2)
        self.total      = round(self.subtotal + self.tax_amount, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "invoice_number": self.invoice_number,
            "created_at": self.created_at.strftime("%d %b %Y"),
            "due_date": self.due_date.strftime("%d %b %Y") if self.due_date else "",
            # "customer_name": self.customer_name,
            # "customer_email": self.customer_email,
            "total": self.total,
            "status": self.status,
        }

class Supplier(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    created_at    = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    name          = db.Column(db.String(120), nullable=False)
    contact_name  = db.Column(db.String(120), default="")
    email         = db.Column(db.String(120), default="")
    phone         = db.Column(db.String(30),  default="")
    abn           = db.Column(db.String(30),  default="")
    address       = db.Column(db.String(200), default="")
    payment_terms = db.Column(db.Integer, default=30)   # days
    notes         = db.Column(db.Text, default="")
    purchases     = db.relationship("PurchaseInvoice", backref="supplier", lazy=True)

    @property
    def total_spent(self):
        return sum(p.total for p in self.purchases if p.status == "paid")

    @property
    def outstanding(self):
        return sum(p.total for p in self.purchases if p.status in ("unpaid", "overdue"))

PURCHASE_CATEGORIES = [
    "Parts & consumables",
    "Tools & equipment",
    "Vehicle & fuel",
    "Insurance",
    "Software & subscriptions",
    "Marketing",
    "Office & admin",
    "Other",
]


class PurchaseInvoice(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    created_at   = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    supplier_id  = db.Column(db.Integer, db.ForeignKey("supplier.id"), nullable=False)
    supplier_ref = db.Column(db.String(80),  default="")   # their invoice number
    invoice_date = db.Column(db.Date, nullable=False, default=date.today)
    due_date     = db.Column(db.Date, nullable=True)
    paid_date    = db.Column(db.Date, nullable=True)
    category     = db.Column(db.String(60),  default="")
    line_items_json = db.Column(db.Text, default="[]")
    subtotal     = db.Column(db.Float, default=0.0)
    tax_rate     = db.Column(db.Float, default=10.0)
    tax_amount   = db.Column(db.Float, default=0.0)
    total        = db.Column(db.Float, default=0.0)
    status       = db.Column(db.String(20), default="unpaid")  # unpaid | paid | overdue
    notes        = db.Column(db.Text, default="")

    @property
    def reference(self):
        return f"PUR-{self.id:04d}"

    @property
    def line_items(self):
        try:
            return loads(self.line_items_json or "[]")
        except Exception:
            return []

    def recalculate(self, items):
        self.line_items_json = dumps(items)
        self.subtotal   = sum(float(i.get("qty", 1)) * float(i.get("unit", 0)) for i in items)
        rate = float(self.tax_rate) if self.tax_rate is not None else 10.0
        self.tax_amount = round(self.subtotal * (rate / 100), 2)
        self.total      = round(self.subtotal + self.tax_amount, 2)

    def to_dict(self):
        return {
            "id":            self.id,
            "reference":     self.reference,
            "supplier":      self.supplier.name if self.supplier else "",
            "supplier_ref":  self.supplier_ref,
            "invoice_date":  self.invoice_date.strftime("%d %b %Y"),
            "due_date":      self.due_date.strftime("%d %b %Y") if self.due_date else "",
            "category":      self.category,
            "total":         self.total,
            "status":        self.status,
        }