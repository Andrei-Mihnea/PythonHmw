#!/bin/bash
set -e

# Extract host and port from DATABASE_URL
HOST_PORT=$(echo "$DATABASE_URL" | sed -e 's/^.*@//' -e 's#/.*##')

# Split host and port
if [[ "$HOST_PORT" == *:* ]]; then
  DB_HOST=$(echo "$HOST_PORT" | cut -d: -f1)
  DB_PORT=$(echo "$HOST_PORT" | cut -d: -f2)
else
  DB_HOST="$HOST_PORT"
  DB_PORT="5432"
fi

echo "[start.sh] Waiting for $DB_HOST:$DB_PORT..."
exec ./wait-for-it.sh "$DB_HOST" "$DB_PORT" -- gunicorn -w 4 -b 0.0.0.0:5000 main:app
