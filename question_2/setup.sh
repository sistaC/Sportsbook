#!/bin/sh
DB_FILE="/app/data/sportbooks.db"
echo "Checking for the existence of database file: ${DB_FILE}"
if [ ! -f "$DB_FILE" -o ! -s "$DB_FILE" ]; then
  echo "Database not initialized yet..."

  echo "Creating database file..."
  mkdir -p $(dirname "$DB_FILE")
  touch "$DB_FILE"

  echo "Done."
fi

echo "Executing database schema..."
sqlite3 "$DB_FILE" < ./schema_sports.sql
sqlite3 "$DB_FILE" < ./schema_events.sql
sqlite3 "$DB_FILE" < ./schema_selections.sql

echo "All set."