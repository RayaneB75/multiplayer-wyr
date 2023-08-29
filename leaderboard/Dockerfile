# 1 Set master image
FROM nginx:stable-alpine

# 2 Set working directory
WORKDIR /usr/share/nginx/html

# 3 Install Additional dependencies
RUN apk update && apk add --no-cache \
build-base shadow vim curl \
php7 \
php7-fpm \
php7-common \
php7-pdo \
php7-pdo_mysql \
php7-mysqli \
php7-mcrypt \
php7-mbstring \
php7-xml \
php7-openssl \
php7-json \
php7-phar \
php7-zip \
php7-gd \
php7-dom \
php7-session \
php7-zlib


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
