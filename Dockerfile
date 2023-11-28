FROM python:3.10-slim-buster

LABEL maintainer="Shayan Ghani <shayanghani1384@gmail.com>"

ENV CONTAINER_EXPORTER_ENV=production CONTAINER_EXPORTER_DEBUG=0

EXPOSE 8000

VOLUME ["/var/run/docker.sock:/var/run/docker.sock"]

WORKDIR /opt/src

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "./start.sh" ]


