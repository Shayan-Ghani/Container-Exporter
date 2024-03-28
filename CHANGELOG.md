# ChangeLog for CXP

Version : 1.1

## Key points
- Updated metrics' names
- resolved Container 'Container Deleting Problem' issue
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