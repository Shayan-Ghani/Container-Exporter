from asyncio import gather, new_event_loop, wait
from aiodocker import Docker 
from docker import from_env as docker_env
from stats import get_docker_stats as stat
from prometheus_client import Gauge, Counter
from prometheus_client.exposition import generate_latest
from flask import Flask, Response, request
from time import time
from configs import config

app = Flask(__name__)

# Create Prometheus gauge metrics for status and stats
container_status = Gauge('docker_container_status', 'Docker container status (1 = running, 0 = not running)', ['container_name'])
container_cpu_percentage = Gauge('docker_container_cpu_percentage', 'Docker container cpu usage', ['container_name'])
container_memory_percentage = Gauge('docker_container_memory_percentage', 'Docker container memory usage in percent', ['container_name'])
container_memory_usage_bytes_total = Gauge('docker_container_memory_usage_bytes_total', 'Docker container memory usage in bytes', ['container_name'])

# Create Prometheus Counter metric for Disk I/O 
disk_io_read_counter = Counter("disk_io_read_bytes_total", "Total number of bytes read from disk", ['container_name'])
disk_io_write_counter = Counter("disk_io_write_bytes_total", "Total number of bytes written to disk", ['container_name'])

# Create Prometheus Counter metric for Network I/O
network_rx_counter = Counter("network_rx_bytes_total", "Total number of bytes received over the network", ['container_name'])
network_tx_counter = Counter("network_tx_bytes_total", "Total number of bytes transmitted over the network", ['container_name'])

# get the data that relates to running containers
def get_offline_container():
    client = docker_env()
    global offline_containers
    offline_containers = client.containers.list()

get_offline_container()
    
# get the data for all containers (killed exited stopped and running)
def get_dynamic_container():
    client = docker_env()
    global dynamic_containers
    dynamic_containers = client.containers.list(all=True)


def update_container_status():
    # update the running container_names that is offline with the status of all containers
    get_dynamic_container()

    for dynamic_container in dynamic_containers:
        if dynamic_container.name in [container.name for container in offline_containers]:
            container_status.labels(container_name=dynamic_container.name).set(1 if dynamic_container.status == "running" else 0)
            print(f"container_status for {dynamic_container.name} is : {dynamic_container.status}")
            
# get containers' stats and update their metrics in async mode
async def container_stats():
    start = time()
    docker = Docker()
    containers = await docker.containers.list()
    tasks = [stat.get_container_stats(container) for container in containers]
    all_stats = await gather(*tasks)
    for stats in all_stats:
        container_cpu_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_cpu_percentage(stats[0]))
        container_memory_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_memory_usage(stats[0])[0])        
        container_memory_usage_bytes_total.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_memory_usage(stats[0])[1])        
        disk_io_read_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_disk_io(stats[0])[0])
        disk_io_write_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_disk_io(stats[0])[1])
        network_rx_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_network_io(stats[0])[0])
        network_tx_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_network_io(stats[0])[1])
        
    print("container_stats{:10.4f}".format(time() - start), "\n")


@app.route('/')
def index():
    return "Welcome To CXP Contianer Exporter For Prometheus."

@app.route('/metrics')
def metrics():    
    start = time()
    try:
        update_container_status()
        loop = new_event_loop()
        t = [loop.create_task(container_stats())]
        loop.run_until_complete(wait(t))
    except Exception as e:
        print(f"Error running script: {str(e)}")
    end = time() - start
    print("metrics{:10.4f}".format(end), "\n")

    # generate the latest value of metrics
    return Response(generate_latest(), mimetype='text/plain')

def create_app():
    app.config.from_object(config.Config)
    return app
