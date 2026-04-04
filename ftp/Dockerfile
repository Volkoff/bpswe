FROM debian:stable-slim

# Install dependencies for building with PostgreSQL support
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and compile pure-ftpd from source
WORKDIR /tmp
RUN wget https://download.pureftpd.org/pub/pure-ftpd/releases/pure-ftpd-1.0.51.tar.gz && \
    tar xzvf pure-ftpd-1.0.51.tar.gz && \
    cd pure-ftpd-1.0.51 && \
    ./configure --with-everything --with-pgsql --with-tls --with-pve && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/pure-ftpd-1.0.51*

# Create system user and group for virtual FTP accounts
# All virtual users in the DB will map to this system user
RUN groupadd -g 1000 ftpgroup && \
    useradd -u 1000 -g ftpgroup -d /dev/null -s /etc ftpuser

# Create directories for config, logs, and sites
# /var/www - shared folder for sites accessible by all services
RUN mkdir -p /usr/local/etc/pure-ftpd /var/log/pure-ftpd /var/www && \
    chown 1000:1000 /var/www

# Export port 21 and passive port range
EXPOSE 21 30000-30009

# Start pure-ftpd via shell to substitute PUBLICHOST variable
# -P $PUBLICHOST - tells the server its "external" address for passive mode
CMD ["/bin/sh", "-c", "pure-ftpd -l pgsql:/etc/pure-ftpd/pureftpd-pgsql.conf -p 30000:30009 -E -j -P $PUBLICHOST -d"]
