FROM php:8.3-apache

# Instalamos dependencias del sistema incluyendo libicu-dev para la extensión intl
RUN apt-get update && apt-get install -y \
    libpng-dev libjpeg-dev libfreetype6-dev libzip-dev zip unzip git libicu-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd zip pdo_mysql intl exif

# Instalamos Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Redirección de Apache a /public
RUN sed -ri -e 's!/var/www/html!/var/www/html/public!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!/var/www/html/public!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

RUN a2enmod rewrite headers

# CORS — allow requests from the Astro frontend (both testing and production domains)
COPY cors.conf /etc/apache2/conf-enabled/cors.conf
WORKDIR /var/www/html
COPY . .

# Instalamos dependencias ignorando restricciones de plataforma si fuera necesario
RUN composer install --no-dev --optimize-autoloader --no-interaction

COPY .env .env
RUN chown -R www-data:www-data /var/www/html

# Ensure the menu-data volume directory is owned by www-data at startup
# (Docker named volumes are mounted as root; this script fixes permissions at runtime)
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
