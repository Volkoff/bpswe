#!/bin/bash
# this reloads apache config without shutting it down
docker exec -it bpswe-apache httpd -t && docker exec -it bpswe-apache httpd -k graceful
