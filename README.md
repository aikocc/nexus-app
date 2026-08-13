# Nexus Diagnostics — Flask App

Full-stack Flask web app for the Nexus Diagnostics mobile mechanic business.

## Structure

```
nexus-app/
├── app.py                          # Main Flask app (routes, models, auth)
├── requirements.txt
├── README.md
└── templates/
    ├── index.html                  # Public homepage + booking form
    ├── confirmation.html           # Booking confirmation (fallback)
    ├── admin_login.html            # Admin login page
    ├── admin_dashboard.html        # Admin booking list + filters
    └── admin_booking_detail.html   # Individual booking management
```

## Setup

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

The app will be available at **http://localhost:5000**

## Routes

| Path | Description |
|---|---|
| `/` | Public homepage with booking form |
| `/book` | POST endpoint — saves booking to DB |
| `/admin` | Admin dashboard (login required) |
| `/admin/login` | Admin login |
| `/admin/booking/<id>` | Booking detail, status update, delete |
| `/admin/api/bookings` | JSON API — all bookings |

## Default admin credentials

```
Username: admin
Password: nexus2026
```

**Change these before going live** — set environment variables:

```bash
export SECRET_KEY="your-secret-key-here"
export ADMIN_USERNAME="yourname"
export ADMIN_PASSWORD="strongpassword"
```

## Database

SQLite by default (`nexus.db` created automatically on first run).

To use PostgreSQL in production, set:
```bash
export DATABASE_URL="postgresql://user:password@host/dbname"
```

## Deploying to production

Recommended: **Railway**, **Render**, or **Fly.io** — all support Flask + SQLite/Postgres out of the box.

For Render:
1. Push this folder to a GitHub repo
2. Create a new Web Service → connect repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add `gunicorn` to requirements.txt
