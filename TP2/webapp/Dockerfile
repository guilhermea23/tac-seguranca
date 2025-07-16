FROM php:8.1-apache

# Instalar dependências e módulos
RUN apt-get update && \
    apt-get install -y curl && \
    docker-php-ext-install mysqli && \
    a2enmod rewrite && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /var/www/html/

RUN chown -R www-data:www-data /var/www/html && \
    find /var/www/html -type d -exec chmod 755 {} \; && \
    find /var/www/html -type f -exec chmod 644 {} \;

EXPOSE 80
CMD ["apache2-foreground"]
