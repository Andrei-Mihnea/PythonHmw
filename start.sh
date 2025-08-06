#!/bin/bash
RAW=$(echo "$DATABASE_URL" | sed -e 's/^.*@//' -e 's#/.*##')
DB_HOST=$(echo "$RAW" | cut -d: -f1)
DB_PORT=$(echo "$RAW" | cut -d: -f2)
DB_PORT=${DB_PORT:-5432}
./wait-for-it.sh "$DB_HOST" "$DB_PORT" -- gunicorn ...