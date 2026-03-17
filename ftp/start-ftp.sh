#!/bin/bash
set -e

echo "⏳ Waiting for PostgreSQL to be available at bpswe-db:5432..."
while ! nc -z bpswe-db 5432; do
  sleep 1
done
echo "✅ PostgreSQL is up! Starting Pure-FTPd..."

# Start Pure-FTPd with PostgreSQL authentication
exec /usr/sbin/pure-ftpd-postgresql \
    -l pgsql:/etc/pure-ftpd/db/postgresql.conf \
    -O w3c:/var/log/pure-ftpd/transfer.log \
    -E -j -R -Y 1 -p 30000:30009
