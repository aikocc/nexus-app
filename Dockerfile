FROM python:3.12-slim

WORKDIR /app

# System deps (kept minimal; add build-essential here if a future dependency needs compiling)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY . .

# SQLite lives here; mount a volume on this path to persist data across container restarts
RUN mkdir -p /app/instance
VOLUME ["/app/instance"]

ENV FLASK_DEBUG=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# app.py creates tables on import (db.create_all()), so gunicorn boots straight into a ready DB
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--preload", "--workers", "2", "app:app"]
