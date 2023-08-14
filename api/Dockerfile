FROM python:3.10.12-slim-bullseye

RUN apt update && apt install \
    ca-certificates \
    cron \
    gcc \
    curl \
    netbase \
    tzdata \
    python3-dev \
    -y && rm -rf /var/lib/apt/lists

RUN mkdir -p /app
WORKDIR /app
COPY /src /app

RUN pip3 install -r /app/requirements.txt

# Hardening
ARG USERID=1000
ARG GROUPID=1000
RUN groupadd --gid $GROUPID gresel && useradd --create-home --shell /bin/bash --uid $USERID --gid $GROUPID uresel
RUN chown -R uresel:gresel /app
USER uresel

RUN mkdir -p /app/logs

# Healthcheck
HEALTHCHECK --interval=5m --timeout=3s \
    CMD curl -f http://localhost:5000/ || exit 1

# Entrypoint
EXPOSE 5000
CMD ["uwsgi", "/app/wsgi.ini"]
