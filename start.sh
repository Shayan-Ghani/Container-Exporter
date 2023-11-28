#!/bin/bash

gunicorn -b 0.0.0.0:8000 -w 3 --access-logfile - --error-logfile - --reload "container_exporter:create_app()"

