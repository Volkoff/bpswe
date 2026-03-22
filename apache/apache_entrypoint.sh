#!/bin/bash
set -e

DOMAIN="tvoje-domena.cz"
EMAIL="tvuj@email.cz"

#CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"

# pokud certifikát neexistuje -> vytvoř ho
#if [ ! -f "$CERT_PATH" ]; then
    #echo "Certifikát neexistuje, generuji..."

    certbot certonly \
        --webroot \
        -w /var/www/certbot \
        -d $DOMAIN \
        --email $EMAIL \
        --agree-tos \
        --no-eff-email \
        --deploy-hook "httpd -k graceful" || echo "Certbot selhal, pokračuji s fallback certem" # aby se použil nový cert
#fi

echo "Certifikát OK"

# obnova na pozadí (každých 12h)
(
while true; do
    certbot renew --quiet && httpd -k graceful
    sleep 12h
done
) &

# spuštění Apache
httpd-foreground
