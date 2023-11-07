#!/bin/bash

CERT_FILE="/etc/ssl/certs/nginx-selfsigned.crt"
KEY_FILE="/etc/ssl/private/nginx-selfsigned.key"

# Check if the certificate file exists
if [ -f "$CERT_FILE" ]; then
    # Check if the certificate is valid
    if openssl x509 -checkend 86400 -noout -in "$CERT_FILE"; then
        echo "Certificate is valid, no need to regenerate."
        exit 0
    else
        echo "Certificate is expired, regenerating..."
    fi
else
    echo "Certificate not found, generating..."
fi

# Generate the certificate and key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=localhost"