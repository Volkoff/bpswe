FROM httpd:2.4

# RUN apt-get update && apt-get install -y \
#     certbot \
#     python3-certbot-apache \
#     openssl

# RUN mkdir -p /var/www/certbot/.well-known/acme-challenge

# # fake cert na začátek
# RUN mkdir -p /etc/letsencrypt/live/tvoje-domena.cz
# RUN openssl req -x509 -nodes -days 1 \
#     -newkey rsa:2048 \
#     -keyout /etc/letsencrypt/live/tvoje-domena.cz/privkey.pem \
#     -out /etc/letsencrypt/live/tvoje-domena.cz/fullchain.pem \
#     -subj "/CN=localhost"



RUN apt-get update && apt-get install -y openssl

# self-signed cert
RUN openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /usr/local/apache2/conf/server.key \
    -out /usr/local/apache2/conf/server.crt \
    -subj "/CN=tvoje-domena.cz"
    # -subj "/CN=localhost"

# zapnutí modulů
RUN sed -i '/LoadModule proxy_module/s/^#//g' /usr/local/apache2/conf/httpd.conf && \
    sed -i '/LoadModule proxy_http_module/s/^#//g' /usr/local/apache2/conf/httpd.conf
    #sed -i '/LoadModule ssl_module/s/^#//g' /usr/local/apache2/conf/httpd.conf && \
    #sed -i '/LoadModule rewrite_module/s/^#//g' /usr/local/apache2/conf/httpd.conf

COPY httpd.conf /usr/local/apache2/conf/httpd.conf


COPY apache_entrypoint.sh /apache_entrypoint.sh
RUN chmod +x /apache_entrypoint.sh

ENTRYPOINT ["/apache_entrypoint.sh"]
