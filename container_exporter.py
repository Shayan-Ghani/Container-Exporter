from aiodocker import Docker
from aiodocker.containers import DockerContainer
from stats import get_docker_stats as stat
from prometheus_client import Gauge, Counter, CONTENT_TYPE_LATEST
from prometheus_client.exposition import generate_latest
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from utils.metrics import PromMetric, prune_stale_metrics, flush_metric_labels
from logging import basicConfig, error, ERROR
from settings.settings import settings

docker_client: Docker

@asynccontextmanager
async def lifespan(app: FastAPI):
    global docker_client
    docker_client = Docker()
        
    yield

    await docker_client.close()

app = FastAPI(lifespan=lifespan)

gauge_container_status = Gauge('cxp_container_status', 'Docker container status (0 = not running, 1 = running, 2 = restarting/unhealthy)', ['container_name'])
gauge_cpu_percentage = Gauge('cxp_cpu_percentage', 'Docker container CPU usage', ['container_name'])
gauge_memory_percentage = Gauge('cxp_memory_percentage', 'Docker container memory usage in percent', ['container_name'])
gauge_memory_bytes = Gauge('cxp_memory_bytes_total', 'Docker container memory usage in bytes', ['container_name'])

counter_disk_read = Counter("cxp_disk_io_read_bytes_total", "Total bytes read from disk", ['container_name'])
counter_disk_write = Counter("cxp_disk_io_write_bytes_total", "Total bytes written to disk", ['container_name'])
counter_net_rx = Counter("cxp_network_rx_bytes_total", "Total bytes received over network", ['container_name'])
counter_net_tx = Counter("cxp_network_tx_bytes_total", "Total bytes sent over network", ['container_name'])


metrics_to_clear: list[PromMetric] = [gauge_cpu_percentage, gauge_memory_percentage, gauge_memory_bytes, counter_disk_read, counter_disk_write, counter_net_rx, counter_net_tx]



async def get_containers(all=False) -> list[DockerContainer]:
    return await docker_client.containers.list(all=all)

def update_container_status(running_containers:list[DockerContainer]):
    for c in running_containers:
        gauge_container_status.labels(container_name=c._container.get("Names")[0][1:]).set(1 if c._container.get('State') == 'running' else 2)

# Async metrics gathering
async def container_stats( running_containers: list[DockerContainer]):
    all_stats = await stat.get_containers_stats(running_containers)
    
    for stats in all_stats:
        name = stats[0]['name'][1:]
        gauge_cpu_percentage.labels(container_name=name).set(stat.calculate_cpu_percentage(stats[0]))
        gauge_memory_percentage.labels(container_name=name).set(stat.calculate_memory_percentage(stats[0]))
        gauge_memory_bytes.labels(container_name=name).set(stat.calculate_memory_bytes(stats[0]))
        disk_read, disk_write = stat.calculate_disk_io(stats[0])
        net_rx, net_tx = stat.calculate_network_io(stats[0])

        counter_disk_read.labels(container_name=name).inc(disk_read)
        counter_disk_write.labels(container_name=name).inc(disk_write)
        counter_net_rx.labels(container_name=name).inc(net_rx)
        counter_net_tx.labels(container_name=name).inc(net_tx)

# List of metrics we want to prune (performance counters)
prunable_metrics: list[PromMetric] = [
    gauge_cpu_percentage, gauge_memory_percentage, gauge_memory_bytes,
    counter_disk_read, counter_disk_write, counter_net_rx, counter_net_tx
]

# Metrics we want to always keep, and set to 0 instead
persistent_metrics: list[PromMetric] = [gauge_container_status]


@app.get("/")
def root():
    return {"message": "Welcome to CXP, Container Exporter for Prometheus."}

@app.get("/metrics")
async def metrics():
    try:
        running_containers = await get_containers()
        update_container_status(running_containers)
        prune_stale_metrics([c._container.get("Names")[0][1:] for c in running_containers], prunable_metrics, persistent_metrics)
        await container_stats(running_containers)
        return PlainTextResponse(
            content=generate_latest(),
            media_type=CONTENT_TYPE_LATEST 
        )
    except Exception as e:
        basicConfig(    
            level=ERROR,
            format='%(asctime)s ERROR %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        error(str(e))
        return PlainTextResponse(f"Error running metrics collection: {str(e)}", status_code=500)