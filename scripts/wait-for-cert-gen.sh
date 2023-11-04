#!/bin/sh

# Loop until the certificate file exists
while [ ! -f /etc/ssl/certs/nginx-selfsigned.crt ]
do
  echo "Waiting for certificate generation..."
  sleep 1
done

# Start the main command
exec "$@"