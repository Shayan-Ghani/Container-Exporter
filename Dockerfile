FROM python:3.10-slim-buster

LABEL maintainer="Shayan Ghani <shayanghani1384@gmail.com>"

ENV CONTAINER_EXPORTER_ENV=production CONTAINER_EXPORTER_DEBUG=0 CONTAINER_EXPORTER_PORT=8000

EXPOSE 8000

VOLUME ["/var/run/docker.sock:/var/run/docker.sock"]

WORKDIR /opt/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x /opt/src/scripts/healthcheck.sh

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=2 \
  CMD /opt/src/scripts/healthcheck.sh

CMD "./start.sh"


