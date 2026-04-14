#!/bin/bash
set -e

HOSTS_FILE="/etc/hosts"

DOMAINS=(
    "www.mojefirma.cz"
    "eshop.mojefirma.cz"
    "blog.mojefirma.cz"
    "admin.mojefirma.cz"
    "ftp.mojefirma.cz"
    "neco.test.mojefirma.cz"
)

for DOMAIN in "${DOMAINS[@]}"; do
    ENTRY="127.0.0.1 $DOMAIN"

    if grep -qE "^[#]*\s*127\.0\.0\.1\s+$DOMAIN(\s|$)" "$HOSTS_FILE"; then
        echo "$DOMAIN už existuje"
    else
        echo "Přidávám $DOMAIN ..."
        echo "$ENTRY" | sudo tee -a "$HOSTS_FILE" > /dev/null
    fi
done

echo "Hotovo."
