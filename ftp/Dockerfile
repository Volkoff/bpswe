FROM debian:bullseye-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y pure-ftpd-postgresql netcat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add a default generic FTP user that owns all web files
RUN groupadd -g 33 www-data || true && \
    useradd -u 33 -g 33 -d /var/www/html -s /usr/sbin/nologin www-data || true

COPY start-ftp.sh /usr/local/bin/start-ftp.sh
RUN chmod +x /usr/local/bin/start-ftp.sh

# Entrypoint is the custom script
CMD ["/usr/local/bin/start-ftp.sh"]
