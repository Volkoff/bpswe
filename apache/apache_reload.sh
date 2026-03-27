#!/bin/bash
docker exec -it bpswe-apache httpd -t && docker exec -it bpswe-apache httpd -k graceful
