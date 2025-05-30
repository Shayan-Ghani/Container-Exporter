# ChangeLog for CXP

---
## [1.2.0] - 2025-05-30

### Changed
- **Internal framework refactor:** Migrated from **Flask** to **FastAPI** for improved asynchronous handling and performance.
- Updated operational dependencies:
  - Added `fastapi`, `uvicorn`
  - Removed `flask`, `gunicorn`

### Notes
- **No changes** to Prometheus metrics endpoints, names, labels, or scrape behavior.
- Existing Prometheus scrapers, dashboards, and alerting rules will continue to work as-is.
- The internal implementation is now fully asynchronous with FastAPI, potentially improving concurrent scrape handling under heavy load.
- Logging and startup messages will differ due to the new framework and ASGI server (`uvicorn`).
- adjust the following settings for `uvicorn` as environment variables:
  - HOST
  - PORT
  - WORKERS (Default : 1)
  - LOG_LEVEL=(Default : warning)

⚠️ **Breaking operational change:** if your deployment or runtime environment specifically depends on Flask or Gunicorn, you'll need to adjust service definitions accordingly.

---

## [1.1.2-1.1.4] 2025-05-05

## Key points
- added Github actions deployment option
- this version makes the code more flexible against vulnerability dependency risks PRs.

**check out README.MD, Deploy with Github Actions to make use of the new changes.**


---

Version : 1.1.1

## Key points
- Updated metrics' names
- resolved Container 'Container Deleting Problem' Issue
- resolved container status update Issue
- added metrics in the format of bytes
 

*Edit your metric names in the following way:*


- `cxp_container_status` : container status (lifecycle)
- `cxp_cpu_percentage`: container cpu usage in percent 
- `cxp_memory_percentage`: container memory usage in percent
- `cxp_memory_bytes_total`: container memory usage in bytes
- `cxp_disk_io_read_bytes_total`: Total number of bytes read from disk
- `cxp_disk_io_write_bytes_total`: Total number of bytes written to disk.
- `cxp_network_rx_bytes_total`: Total number of bytes received over the network
- `cxp_network_tx_bytes_total`: Total number of bytes transmitted over the network

