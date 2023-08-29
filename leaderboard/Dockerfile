# 1 Set master image
FROM nginx:stable-alpine

# 2 Set working directory
WORKDIR /usr/share/nginx/html

# 3 Install Additional dependencies
RUN apk update && apk add --no-cache \
build-base shadow vim curl \
php \
php-fpm \
php-common \
php-pdo \
php-pdo_mysql \
php-mysqli \
php-mbstring \
php-xml \
php-openssl \
php-json \
php-phar \
php-zip \
php-gd \
php-dom \
php-session \
php-zlib


# 4 Remove Cache
RUN rm -rf /var/cache/apk/*

# 5 Remove default nginx website
RUN rm /etc/nginx/conf.d/default.conf

# 6 Nginx Configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 7 Copy existing application directory permissions
COPY  src/ /usr/share/nginx/html

RUN php-fpm


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
