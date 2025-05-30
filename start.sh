#!/bin/sh

# Configurable variables
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-1}
LOG_LEVEL=${LOG_LEVEL:-warning}

echo "Starting Container Exporter..."
echo "Host: $HOST, Port: $PORT, Workers: $WORKERS, Log Level: $LOG_LEVEL"

# Trap signals to shut down gracefully
term_handler() {
  echo "SIGTERM received, shutting down..."
  kill -TERM "$child" 2>/dev/null
  wait "$child"
  exit 0
}
trap term_handler SIGTERM

while true; do
  uvicorn "container_exporter:app" \
    --host "$HOST" \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level "$LOG_LEVEL"

  echo "Uvicorn crashed with exit code $?. Restarting in 3 seconds..."
  sleep 3
done
