# Build
FROM debian:12.1-slim as build

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y curl git wget unzip libgconf-2-4 gdb libstdc++6 libglu1-mesa fonts-droid-fallback lib32stdc++6 python3
RUN apt-get clean

# download Flutter SDK from Flutter Github repo
RUN git clone https://github.com/flutter/flutter.git /usr/local/flutter
# Set flutter environment path
ENV PATH="/usr/local/flutter/bin:/usr/local/flutter/bin/cache/dart-sdk/bin:${PATH}"

# Run flutter doctor
RUN flutter doctor

# Enable flutter web
RUN flutter channel stable
RUN flutter upgrade
RUN flutter config --enable-web

RUN mkdir -p /app

COPY . /app

WORKDIR /app

RUN flutter pub get
RUN flutter build web --dart-define=FRONT_TOKEN=$FRONT_TOKEN --dart-define=API_SRV_PROTOCOL=$API_SRV_PROTOCOL \
    --dart-define=API_SRV_HOSTNAME=$API_SRV_HOSTNAME --dart-define=API_SRV_PORT=$API_SRV_PORT

# Deploy
FROM nginx:stable-alpine

# Remove the default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the built web app from the build stage
COPY --from=build /app/build/web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
