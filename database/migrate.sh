#!/bin/bash
# Database migration script

set -e

DB_NAME="tango"
DB_USER="tango"
DB_PASS="tango"
DB_HOST="localhost"

echo "Running database migrations..."

# Backup current database
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql

# Apply schema
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME < schema.sql

echo "Migrations completed successfully"
