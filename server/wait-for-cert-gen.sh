#!/bin/sh

# Loop until the certificate file exists
while [ ! -f /etc/ssl/certs/nginx-selfsigned.crt ]
do
  echo "Waiting for certificate generation..."
  sleep 1
done

echo "Found certificate, starting server..."

# Start the main command
exec "$@"