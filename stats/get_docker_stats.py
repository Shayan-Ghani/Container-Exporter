import docker
import time
import asyncio

def calculate_cpu_percentage(stats):
    cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
    system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
    number_cpus = stats['cpu_stats']['online_cpus'] 
    cpu_percent = (cpu_delta / system_delta) * number_cpus * 100.0 
    
    return cpu_percent

def calculate_memory_percentage(stats):
    memory_usage = stats['memory_stats']['usage']
    memory_limit = stats['memory_stats']['limit']

    memory_percent = (memory_usage / memory_limit) * 100.0

    return memory_percent
    
def calculate_disk_io(stats):
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

def calculate_network_io(stats):
    network_rx_bytes = 0
    network_tx_bytes = 0

    if "networks" in stats:
        networks = stats["networks"]

        for network in networks.values():
            network_rx_bytes += network["rx_bytes"]
            network_tx_bytes += network["tx_bytes"]

    return network_rx_bytes, network_tx_bytes

async def get_container_stats(container):
    stats = await container.stats(stream=False)
    return stats



# def test_stats(stats):
#     start_stat = time.time()    
#     memory_stats = stats['memory_stats']
#     cpu_stats = stats['cpu_stats']
#     precpu_stats = stats['precpu_stats']


#     res = {
#         "memory_usage": memory_stats['usage'],
#         "memory_limit": memory_stats['limit'],
#         "total_cpu_usage": cpu_stats['cpu_usage']['total_usage'],
#         "total_precpu_usage": precpu_stats['cpu_usage']['total_usage'],
#         "system_cpu_usage": cpu_stats['system_cpu_usage'],
#         "system_precpu_usage": precpu_stats['system_cpu_usage'],
#         "cpu_percent_len": len(stats['cpu_stats']['cpu_usage']['percpu_usage'])
#     }

#     end_stat = time.time() - start_stat
#     print("res {:10.4f}".format(end_stat), "\n")   
#     return res
