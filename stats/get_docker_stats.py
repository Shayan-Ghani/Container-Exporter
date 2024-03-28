def calculate_cpu_percentage(stats) -> float:
    cpu_percent = 0
    
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    number_cpus = stats['cpu_stats']['online_cpus'] 
    if cpu_delta is not None and system_delta is not None and number_cpus is not None:
        cpu_percent = (cpu_delta / system_delta) * number_cpus * 100.0 
    
    return cpu_percent

def calculate_memory_percentage(stats) -> float:
    memory_percent = 0
    memory_usage_bytes = 0
    
    memory_usage_bytes = stats['memory_stats']['usage']
    memory_limit = stats['memory_stats']['limit']
    if memory_usage_bytes is not None and memory_limit is not None:
        memory_percent = (memory_usage_bytes / memory_limit) * 100.0

    return memory_percent

def calculate_memory_bytes(stats) -> bytes:
    memory_usage_bytes = stats['memory_stats']['usage']
    if memory_usage_bytes is not None:
        return memory_usage_bytes
    return 0
    
def calculate_disk_io(stats) -> bytes:
    disk_io_read = 0
    disk_io_write = 0

    if "blkio_stats" in stats and "io_service_bytes_recursive" in stats["blkio_stats"]:
        io_service_bytes_recursive = stats["blkio_stats"]["io_service_bytes_recursive"]

        if io_service_bytes_recursive is not None:
            for io_stat in io_service_bytes_recursive:
                if "op" in io_stat and "value" in io_stat:
                    if io_stat["op"] == "read":
                        disk_io_read += io_stat["value"]
                    elif io_stat["op"] == "write":
                        disk_io_write += io_stat["value"]

    return disk_io_read, disk_io_write

def calculate_network_io(stats) -> bytes:
    network_rx_bytes = 0
    network_tx_bytes = 0

    if "networks" in stats:
        networks = stats["networks"]
        if networks is not None:
            for network in networks.values():
                network_rx_bytes += network["rx_bytes"]
                network_tx_bytes += network["tx_bytes"]

    return network_rx_bytes, network_tx_bytes

async def get_container_stats(container):
    stats = await container.stats(stream=False)
    return stats