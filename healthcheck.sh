#!/bin/bash

log_dir="/opt/src/logs"
mkdir -p $log_dir

if ! curl http://localhost:8000/ > "${log_dir}/index.txt"; then
  echo "Port 8000 not responding"
  exit 1
fi


if ! curl --max-time 6 --silent --show-error http://localhost:8000/metrics > "${log_dir}/metrics.txt"; then
  echo "/metrics endpoint not responding"
  cat "${log_dir}/metrics.txt"
  exit 1
fi


exit 0
