#!/bin/bash
set -e

# Extract host from DATABASE_URL
DB_HOST=$(echo "$DATABASE_URL" | sed -e 's/^.*@//' -e 's#/.*##')

# Extract port if present
DB_PORT=$(echo "$DB_HOST" | cut -s -d: -f2)
DB_HOST=$(echo "$DB_HOST" | cut -d: -f1)

# Fallback to default port
DB_PORT=${DB_PORT:-5432}

echo "[start.sh] Waiting for $DB_HOST:$DB_PORT..."
./wait-for-it.sh "$DB_HOST" "$DB_PORT" -- gunicorn -w 4 -b 0.0.0.0:5000 main:app
