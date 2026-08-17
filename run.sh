#!/usr/bin/env bash
# Local dev runner for Nexus Diagnostics.
# Creates a venv on first run, installs deps, loads .env if present, then starts the app.
set -e

cd "$(dirname "$0")"

# 1. Create venv if it doesn't exist yet
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# 2. Activate it
source venv/bin/activate

# 3. Install/update dependencies
pip install -q -r requirements.txt

# 4. Load .env file if present (SECRET_KEY, ADMIN_USERNAME, ADMIN_PASSWORD, DATABASE_URL, etc.)
if [ -f ".env" ]; then
    echo "Loading .env"
    set -a
    source .env
    set +a
fi

# 5. Run the dev server
echo "Starting Nexus Diagnostics at http://localhost:5000"
python app.py
