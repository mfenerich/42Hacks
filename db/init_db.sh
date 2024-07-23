#!/bin/bash
set -e

# Debug: Print environment variables
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"

# Function to check PostgreSQL readiness using psql
function check_pg_ready() {
  psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' > /dev/null 2>&1
}

echo "Waiting for PostgreSQL to start..."

# Wait for PostgreSQL to be ready
until check_pg_ready; do
  echo "PostgreSQL is not ready yet. Retrying..."
  sleep 2
done

echo "PostgreSQL is up and running."

# Run the init.sql script
# psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f /docker-entrypoint-initdb.d/init.sql

echo "Database initialized."
