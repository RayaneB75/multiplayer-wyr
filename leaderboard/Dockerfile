# 1 Set master image
FROM nginx:stable-alpine

# 2 Set working directory
WORKDIR /usr/share/nginx/html

# 5 Remove default nginx website
RUN rm /etc/nginx/conf.d/default.conf

# 6 Nginx Configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 7 Copy existing application directory permissions
COPY  src/ /usr/share/nginx/html
