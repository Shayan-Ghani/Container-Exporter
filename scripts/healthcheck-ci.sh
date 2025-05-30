#!/bin/bash

set -e

log_dir="/opt/src/logs"
mkdir -p "$log_dir"

container_name="healthcheck_test_container"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
  echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

pass() {
  echo -e "${GREEN}✅ $1${NC}"
}

fail() {
  echo -e "${RED}❌ $1${NC}"
  [ -n "$container_name" ] && docker rm -f "$container_name" >/dev/null 2>&1 || true
  exit 1
}

log "Starting CI Healthcheck..."

log "Spinning up test container: $container_name"
docker run -d --name "$container_name" alpine sleep 60 >/dev/null || fail "Failed to start container"

log "Checking root endpoint..."
if curl --silent --fail http://localhost:8000/ > "${log_dir}/index.txt"; then
  pass "Root endpoint responded successfully."
else
  fail "Port 8000 not responding."
fi

log "Checking /metrics endpoint..."
if curl --max-time 6 --silent --show-error http://localhost:8000/metrics > "${log_dir}/metrics.txt"; then
  pass "/metrics endpoint responded successfully."
else
  fail "/metrics endpoint not responding."
fi

log "Displaying container-related metrics:"
echo -e "\n${GREEN}--- Metrics with container added ---${NC}"
grep 'container_name' "${log_dir}/metrics.txt" | sort | uniq || echo "(No container metrics found)"

log "Removing test container..."
docker rm -f "$container_name" >/dev/null || fail "Failed to remove test container"

log "Waiting 5s for app to reflect container removal..."
sleep 1

log "Checking /metrics endpoint again after container removal..."
if curl --max-time 6 --silent --show-error http://localhost:8000/metrics > "${log_dir}/metrics_post_remove.txt"; then
  pass "/metrics endpoint responded successfully post-removal."
else
  fail "/metrics endpoint not responding after container removal."
fi

log "Displaying container-related metrics after removal:"
echo -e "\n${GREEN}--- Metrics after container removed ---${NC}"
grep 'container_name' "${log_dir}/metrics_post_remove.txt" | sort | uniq || echo "(No container metrics found)"

pass "Full Healthcheck Completed Successfully."

exit 0
