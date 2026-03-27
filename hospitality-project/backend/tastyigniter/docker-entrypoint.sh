#!/bin/sh
# Fix ownership of the menu-data volume so www-data can write JSON files
mkdir -p /var/www/data
chown www-data:www-data /var/www/data

# Hand off to default php:apache entrypoint, then Apache
exec /usr/local/bin/docker-php-entrypoint apache2-foreground
