from aiodocker.docker import DockerContainer
from asyncio import gather

def calculate_cpu_percentage(stats: dict) -> float:
    cpu_stats    = stats.get('cpu_stats', {})
    precpu_stats = stats.get('precpu_stats', {})
    total       = cpu_stats.get('cpu_usage', {}).get('total_usage')
    prev_total  = precpu_stats.get('cpu_usage', {}).get('total_usage')
    system      = cpu_stats.get('system_cpu_usage')
    prev_system = precpu_stats.get('system_cpu_usage')
    n_cpus      = cpu_stats.get('online_cpus')

    if None in (total, prev_total, system, prev_system, n_cpus):
        return 0.0

    cpu_delta    = total - prev_total
    system_delta = system - prev_system
    
    if system_delta <= 0:
        return 0.0

    return (cpu_delta / system_delta) * n_cpus * 100.0


def calculate_memory_percentage(stats: dict) -> float:
    mem_stats = stats.get('memory_stats', {})
    usage     = mem_stats.get('usage')
    limit     = mem_stats.get('limit')

    if usage is None or limit is None or limit == 0:
        return 0.0

    return (usage / limit) * 100.0


def calculate_memory_bytes(stats) -> float:
    mem_stats = stats.get('memory_stats', {}) or {}
    memory_usage_bytes = mem_stats.get('usage')
    
    if memory_usage_bytes is not None:
        return memory_usage_bytes
    return 0.0
    
def calculate_disk_io(stats: dict) -> bytes:
    disk_io_read = 0
    disk_io_write = 0

    io_list = stats.get("blkio_stats", {}) \
                .get("io_service_bytes_recursive") or []

    for io_stat in io_list:
        op    = io_stat.get("op")
        value = io_stat.get("value", 0)
        if op == "read":
            disk_io_read  += value
        elif op == "write":
            disk_io_write += value


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

async def get_containers_stats(containers:list[DockerContainer]):
    tasks = [container.stats(stream=False) for container in containers]
    return await gather(*tasks)