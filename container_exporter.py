from asyncio import gather, new_event_loop, wait
from aiodocker import Docker 
from docker import from_env as docker_env
from stats import get_docker_stats as stat
from prometheus_client import Gauge, Counter
from prometheus_client.exposition import generate_latest
from flask import Flask, Response, request
from configs import config

app = Flask(__name__)


# TO-DO : add change log
# TO-DO : modulization

# Create Prometheus gauge metrics for status and stats
container_status = Gauge('cxp_container_status', 'Docker container status (1 = running, 0 = not running)', ['container_name'])
container_cpu_percentage = Gauge('cxp_cpu_percentage', 'Docker container cpu usage', ['container_name'])
container_memory_percentage = Gauge('cxp_memory_percentage', 'Docker container memory usage in percent', ['container_name'])
container_memory_bytes_total = Gauge('cxp_memory_bytes_total', 'Docker container memory usage in bytes', ['container_name'])

# Create Prometheus Counter metric for Disk I/O 
disk_io_read_counter = Counter("cxp_disk_io_read_bytes_total", "Total number of bytes read from disk", ['container_name'])
disk_io_write_counter = Counter("cxp_disk_io_write_bytes_total", "Total number of bytes written to disk", ['container_name'])

# Create Prometheus Counter metric for Network I/O
network_rx_counter = Counter("cxp_network_rx_bytes_total", "Total number of bytes received over the network", ['container_name'])
network_tx_counter = Counter("cxp_network_tx_bytes_total", "Total number of bytes transmitted over the network", ['container_name'])
    

metrics_names = [container_cpu_percentage,  container_memory_percentage ,  container_memory_bytes_total , disk_io_read_counter , disk_io_write_counter , network_rx_counter ,  network_tx_counter ] 

def flush_metric_labels(metrics:list):
    for m in metrics:
        m.clear()
   
# get the data that relates to running containers at the first startup
def get_init_container():
    client = docker_env()
    global init_containers
    init_containers = client.containers.list()

get_init_container()
    
# get the data for all containers (killed exited stopped and running)
def get_all_container():
    client = docker_env()
    global all_containers
    all_containers = client.containers.list(all=True)


def update_container_status():
    # update the running container_names that is offline with the status of all containers
    get_all_container()
    for container in all_containers:
        if container.status != "running":
            flush_metric_labels(metrics_names)
        if container.name in [c.name for c in init_containers]:
            container_status.labels(container_name=container.name).set(1 if container.status == "running" else 0)

    for removed_container in init_containers:
        if removed_container.name not in [c.name for c in all_containers]:
            container_status.labels(container_name=removed_container.name).set(0)    

# get containers' stats and update their metrics in async mode
async def container_stats():
    docker = Docker()
    containers = await docker.containers.list()
    tasks = [stat.get_container_stats(container) for container in containers]
    all_stats = await gather(*tasks)
    for stats in all_stats:
        container_cpu_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_cpu_percentage(stats[0]))
        container_memory_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_memory_percentage(stats[0]))        
        container_memory_bytes_total.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_memory_bytes(stats[0]))       
        disk_io_read_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_disk_io(stats[0])[0])
        disk_io_write_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_disk_io(stats[0])[1])
        network_rx_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_network_io(stats[0])[0])
        network_tx_counter.labels(container_name=stats[0]['name'][1:]).inc(stat.calculate_network_io(stats[0])[1])


@app.route('/')
def index():
    return "Welcome To CXP, Contianer Exporter For Prometheus."

@app.route('/metrics')
def metrics():    
    try:
        update_container_status()
        loop = new_event_loop()
        t = [loop.create_task(container_stats())]
        loop.run_until_complete(wait(t))
    except Exception as e:
        return f"Error running script: {str(e)}"

    # generate the latest value of metrics
    return Response(generate_latest(), mimetype='text/plain')

def create_app():
    app.config.from_object(config.Config)
    return app

if __name__ == "__main__":
    app.run('0.0.0.0', 8000)