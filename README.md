# Nexus Diagnostics

A Flask web application for **Nexus Diagnostics**, a mobile vehicle diagnostics business. The platform includes a public marketing site with online booking, a customer portal, and a full admin back-office for managing leads, bookings, customers, vehicles, and tax invoices.

> ⚠️ This codebase appears to be a work-in-progress / workshop-style project (see `README` origins below). Some routes reference models/fields (e.g. `registration_number` vs `registration_no`) that don't fully match `models.py` — see [Known Issues](#known-issues) before deploying.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Data Model](#data-model)
- [Application Areas](#application-areas)
  - [Public Site](#public-site)
  - [Customer Portal](#customer-portal)
  - [Admin Panel](#admin-panel)
  - [API Endpoints](#api-endpoints)
- [Third-Party Integrations](#third-party-integrations)
- [Blueprint Auto-Registration](#blueprint-auto-registration)
- [Frontend Notes](#frontend-notes)
- [Known Issues](#known-issues)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Nexus Diagnostics is a mobile mechanic / vehicle diagnostics service. Customers can request a diagnostic booking from the public site, which becomes a **Lead**. Admin staff review leads and convert them into a full **Booking**, linked to a **Customer** and **Vehicle** record. Admins can also generate professional, print-ready **tax invoices**, look up vehicle details by registration/VIN via the EzyParts trade portal, and manage the customer/vehicle database directly.

The app is built with Flask, using SQLAlchemy for the ORM, Flask-WTF for forms/CSRF protection, and server-rendered Jinja2 templates (UIkit for the admin/customer shell, a custom design system for the public marketing site).

---

## Features

- 🏠 **Public marketing site** — hero, services, live "diagnostic feed" widget, booking form with Google Places address autocomplete
- 📋 **Lead capture & conversion** — public bookings are captured as Leads, then converted into full Bookings by admin staff
- 📅 **Booking management** — list view (filterable/paginated), calendar view, and a time-slot day view with overlapping-event lane layout, all loaded via AJAX
- 👤 **Customer & vehicle CRM** — searchable customer and vehicle records with full CRUD
- 🚗 **Vehicle rego/VIN lookup** — integrates with the EzyParts (Burson) trade portal to pull make/model/series/engine/transmission data automatically
- 🧾 **Dynamic tax invoice builder** — drag-and-drop line items, notes, and grouped "packages," automatic GST-inclusive totals, multi-page pagination, and JSON save/load for draft invoices
- 🌐 **REST-ish JSON API** — customer/vehicle search and detail endpoints for autocomplete widgets
- 🔐 **CSRF protection** site-wide via Flask-WTF, with explicit exemptions for JSON API POSTs
- 🧩 **Auto-discovered blueprints** — new route modules are picked up automatically, no manual registration needed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | Flask 3.0 |
| ORM | Flask-SQLAlchemy 3.1 / SQLAlchemy 2.0 |
| Forms & CSRF | Flask-WTF / WTForms |
| Database | SQLite by default (`workshop.db`), configurable via `DATABASE_URL` |
| Templating | Jinja2 |
| Admin/Customer UI | UIkit 3.21 |
| Public site UI | Custom CSS (`static/css/style.css`) with Space Grotesk / Inter / JetBrains Mono |
| HTTP client (integrations) | `requests` |
| Env config | `python-dotenv` |

See [`requirements.txt`](requirements.txt) for pinned versions.

---

## Project Structure

```
flask_workshop/
├── app.py                     # App factory, template filters, error handlers
├── extensions.py               # db (SQLAlchemy) and csrf (CSRFProtect) singletons
├── models.py                   # Customer, Vehicle, Lead, Booking models
├── seed_data.py                 # Sample/demo data seeding scripts
├── requirements.txt
│
├── forms/
│   ├── admin/                  # CustomerForm, VehicleForm, LeadForm, BookingForm
│   ├── customer/                # CustomerProfileForm
│   └── public/                  # LoginForm, RegistrationForm, BookingForm
│
├── routes/
│   ├── __init__.py              # Recursive blueprint auto-registration
│   ├── admin/                   # dashboard, leads, bookings, customers, vehicles, invoices, reports
│   ├── api/                     # JSON API: customers, vehicles, EzyParts lookup, address autocomplete
│   ├── customer/                 # customer dashboard, vehicles, appointments
│   └── public/                   # main site, services, auth
│
├── templates/
│   ├── base.html                # Root layout, shared toast component
│   ├── admin/                    # Admin shell + dashboard, leads, bookings, customers, vehicles, invoices, reports
│   ├── customer/                 # Customer portal shell + dashboard, vehicles, appointments
│   ├── public/                   # Public site pages (index, services, about, contact, login, register)
│   └── errors/                   # 404 / 500 pages
│
├── static/
│   └── css/                      # style.css (public/shell design system), uikit-theme.css (UIkit overrides)
│
└── utils/
    ├── ezyparts.py                # EzyParts (Burson) vehicle lookup client
    ├── google_places.py           # Google Places Autocomplete client
    └── vehicle_parser.py          # Normalizes rego-lookup API responses into vehicle variants
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- A virtual environment tool (`venv` recommended)

### Installation

```bash
git clone <repository-url>
cd flask_workshop

python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///workshop.db

# EzyParts (Burson) trade portal — required for rego/VIN lookup
EZYPARTS_ACCOUNT=
EZYPARTS_USERNAME=
EZYPARTS_PASSWORD=

# Google Places API — required for address autocomplete on the booking form
GOOGLE_PLACES_API_KEY=
```

### Run the App

The app factory lives in `app.py`:

```bash
python app.py
```

By default this runs with `debug=True` on `http://0.0.0.0:5000`. Database tables are created automatically on startup via `db.create_all()` inside the app context — no separate migration step is required for a fresh SQLite DB.

### Seeding Sample Data

`seed_data.py` contains helper functions for populating customers, vehicles, leads, and bookings (including day/week booking generators for testing the calendar and day views):

```bash
python seed_data.py
```

> Note: the top portion of `seed_data.py` (`seed_database()`) is currently commented out; the script's `__main__` block runs `seed_bookings()`, `seed_specific_day_bookings()`, and `seed_booking_with_customer_and_vehicle()`, which expect customers/vehicles to already exist.

---

## Configuration

Configuration is loaded from environment variables in `app.py`:

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key` | Flask session/CSRF signing key |
| `DATABASE_URL` | `sqlite:///workshop.db` | SQLAlchemy database URI |
| `EZYPARTS_ACCOUNT` / `EZYPARTS_USERNAME` / `EZYPARTS_PASSWORD` | — | Credentials for the EzyParts trade portal (`utils/ezyparts.py`) |
| `GOOGLE_PLACES_API_KEY` | — | Google Places Autocomplete key (`utils/google_places.py`) |
| `EZYPARTS_SESSION_FILE` | `~/.ezyparts_session.json` | Optional override for where EzyParts session cookies are cached |

---

## Data Model

Defined in `models.py`, all models use SQLAlchemy's declarative style via the shared `db` instance.

### `Customer`
Core CRM record. Supports individuals and companies (`is_company`, `company_name`, `tax_id`). Has a one-to-many relationship to `Vehicle` (cascading delete) and `Booking`.

### `Vehicle`
Belongs to a `Customer`. Stores registration/VIN/chassis identifiers plus make/model/series/year/body/drive/fuel/transmission/engine specs, odometer, and notes.

### `Lead`
A raw inbound booking request from the public site (name, contact info, rego, vehicle description, address, notes). Leads can be `converted` into a `Booking`, tracked via `booking_id` / `converted_at`.

### `Booking`
The core scheduling record. Stores **snapshots** of customer and vehicle data at time of booking (so historical bookings remain accurate even if the customer/vehicle record later changes), plus service details, scheduling fields (`preferred_date`/`scheduled_date`/`scheduled_time`/`duration_minutes`), `status`, and `priority`. Includes helper methods: `link_to_customer()`, `link_to_vehicle()`, `sync_from_lead()`, `confirm()`, `complete()`, `cancel()`, and `generate_booking_number()` (format `BK-YYYYMMDD-XXXX`).

**Booking status values:** `pending`, `confirmed`, `in_progress`, `completed`, `cancelled`, `no_show`
**Priority values:** `low`, `normal`, `high`, `urgent`

---

## Application Areas

### Public Site
_Blueprint prefix: `/`, `/services`, `/auth`_

- `/` — Landing page with hero, live diagnostic widget, service pricing grid, and an inline booking form (submits a `Lead` via AJAX or standard POST)
- `/services` — Service list with pricing/duration
- `/about`, `/contact` — Static informational pages
- `/auth/login`, `/auth/register`, `/auth/logout` — Staff/customer authentication pages (forms are present; full auth logic is not yet wired up)

The booking form (`templates/public/index.html`) includes a custom-built, dependency-free address autocomplete widget backed by `/api/address-autocomplete`.

### Customer Portal
_Blueprint prefix: `/customer`_

- `/customer/` — Dashboard showing vehicle count and registered vehicles
- `/customer/vehicles/` — List of the customer's vehicles
- `/customer/appointments/` — Upcoming appointments (currently returns an empty list — not yet wired to the `Booking` model)

### Admin Panel
_Blueprint prefix: `/admin`_

| Route | Purpose |
|---|---|
| `/admin/` | Dashboard: customer/vehicle counts, recent customers |
| `/admin/leads/` | Lead list and detail view; converts a lead into a `Booking` and links to existing customer/vehicle records by email/rego match |
| `/admin/bookings/` | Full booking management: **list** (search/filter/paginate), **calendar** (month grid with per-day booking badges), and **day** (time-slot grid with overlapping-lane layout) views, all swapped in via AJAX without a full page reload |
| `/admin/bookings/<id>` | View/edit a single booking; confirm/complete/cancel/delete actions |
| `/admin/customers/` | Customer CRUD with search |
| `/admin/vehicles/` | Vehicle CRUD, including a **rego lookup** tool that queries EzyParts and lets the admin pick from multiple returned variants |
| `/admin/invoices/` | Dynamic tax invoice builder — add line items, standalone notes, or bundled "packages" (with their own sub-items and running subtotal); supports drag-and-drop reordering, auto-calculated GST-inclusive totals, JSON export/import of a draft, and renders a paginated, print-ready A4 invoice (`template.html`) |
| `/admin/reports/` | Placeholder reports dashboard (customer/vehicle counts; revenue/report links not yet implemented) |

### API Endpoints
_Blueprint prefix: `/api`_

| Endpoint | Method | Description |
|---|---|---|
| `/api/customers/search?q=` | GET | Multi-word ILIKE search across name, email, phone, mobile, company |
| `/api/customers/<id>` | GET | Full customer detail JSON |
| `/api/customers/<id>/vehicles` | GET | Vehicles belonging to a customer |
| `/api/vehicles/search?q=` | GET | Search vehicles by rego, VIN, make, model |
| `/api/vehicles/<id>` | GET | Full vehicle detail JSON |
| `/api/lookup-rego` | POST | Looks up a vehicle by rego + state via EzyParts and returns parsed variant options |
| `/api/address-autocomplete?q=` | GET | Proxies Google Places Autocomplete, biased to the Canberra/ACT area |

There is also a secondary, older set of autocomplete endpoints under `/admin/bookings/api/customers/search` and `/admin/bookings/api/vehicles/search` defined directly in `routes/admin/bookings.py` (see [Known Issues](#known-issues)).

---

## Third-Party Integrations

### EzyParts (`utils/ezyparts.py`)
A hand-rolled client that replicates the `ezyparts.burson.com.au` trade portal's internal AJAX flow:

1. **Search** by VIN (`/vehicle/t/search`) or rego (`/vehicle/rego/search` + `/vehicle/rego/search/more`)
2. **Detail lookup** (`/vehicle/{id}/details`) for full spec data

Handles session-cookie login, caches cookies to disk (`~/.ezyparts_session.json` by default, `chmod 600`), and re-authenticates automatically when the cached session expires. Raises `EzyPartsError` on login/parsing failures.

### Google Places (`utils/google_places.py`)
Wraps the Google Places Autocomplete and Place Details REST APIs, restricted to Australian addresses and biased toward Canberra, ACT (50km radius). Used by the public booking form's address field.

### Vehicle Response Parser (`utils/vehicle_parser.py`)
Normalizes the differently-shaped JSON responses from EzyParts's rego/VIN search into a consistent list of vehicle "variants" (make/model/sub-model/series/year/body/drive/fuel/transmission/chassis), so the admin can pick the correct match when a rego returns multiple candidate vehicles.

---

## Blueprint Auto-Registration

Rather than manually importing and registering every blueprint, `routes/__init__.py` walks the `routes/` package tree recursively (`pkgutil.iter_modules`) and registers any `Blueprint` instance it finds on any module. This means **adding a new route module under `routes/<area>/` is automatically picked up** — no changes to `app.py` are needed as long as the module defines a top-level `Blueprint`.

---

## Frontend Notes

- **Public site & customer/admin shell** share `templates/base.html`, which loads Google Fonts (Space Grotesk / Inter / JetBrains Mono), UIkit 3.21 (JS+CSS+icons), and the project's own `static/css/style.css` + `static/css/uikit-theme.css`.
- The **admin bookings list** (`templates/admin/bookings/list.html`) is a fairly involved piece of vanilla JS: it manages three views (list/calendar/day) all fetched via `fetch()` + `X-Requested-With: XMLHttpRequest`, swaps `#booking-content` in place, and keeps the URL/query string in sync with `history.pushState`.
- The **invoice builder** (`templates/admin/invoices/create.html`) is a large self-contained vanilla JS module supporting drag-and-drop line-item reordering, three item "modes" (line item / note / package), live GST-inclusive total calculation, and full JSON export/import of the draft invoice.

---

## Known Issues

This project has a few loose ends worth being aware of before relying on it in production:

- **Field name mismatches**: `routes/admin/bookings.py`'s legacy `/api/vehicles/search` and `new_booking()` reference `Vehicle.registration_number`, but the model defines `registration_no`.
- **`admin_leads.view_lead`** references `datetime.utcnow()` without importing `datetime` as a class-level attribute correctly in all code paths — double check imports if extending.
- **CSRF exemption**: `admin_invoices.create_invoice` is explicitly exempted from CSRF (`@csrf.exempt`) — the invoice form does not currently include a CSRF token relative to that exemption.
- **Auth is not implemented**: `LoginForm`/`RegistrationForm` render pages but there's no session/login backend wired up yet — all `/admin` and `/customer` routes are currently open.
- **Customer appointments** (`/customer/appointments/`) always returns an empty list; it isn't yet querying `Booking` by the logged-in customer.
- **`seed_data.py`** contains two generations of seed logic (a large commented-out `seed_database()` plus an active booking-seeding section) — review before running against a database you care about.

---

## Contributing

Issues, fixes, and suggestions are welcome — open a pull request or file an issue describing the change.

## License

This project is intended for educational/workshop use. Add a formal license (e.g. MIT) here if you intend to distribute it.
