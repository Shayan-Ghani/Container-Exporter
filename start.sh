#!/bin/sh

port="$1"
gunicorn -b 0.0.0.0:$port -w 3 --access-logfile - --error-logfile - --reload "container_exporter:create_app()"

