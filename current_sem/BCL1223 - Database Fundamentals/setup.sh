#!/bin/bash
# Setup script for BCL1223 Oracle Database
# Run this after container is healthy: docker-compose up -d && sleep 300 && ./setup.sh

echo "Setting up BCL1223 database..."

# Wait for Oracle to be ready
echo "Waiting for Oracle to be ready..."
until sqlplus -L system/OraclePass123@//localhost:1521/XEPDB1 @/dev/null &>/dev/null; do
    echo "Oracle not ready yet, waiting..."
    sleep 10
done

echo "Oracle is ready. Setting up BCL1223 schema..."

# Create user and run init
sqlplus system/OraclePass123@//localhost:1521/XEPDB1 @init.sql

echo "Setup complete!"
echo ""
echo "Connection details:"
echo "  Host: localhost"
echo "  Port: 1521"
echo "  Service: XEPDB1"
echo "  Username: bcl1223"
echo "  Password: bcl1223"
