from docker import from_env as docker_env
from prometheus_client import Gauge
# get the data that relates to running containers at the first startup
def get_init_container():
    client = docker_env()
    return client.containers.list()

init_containers_names = [c.name for c in get_init_container()]


def update_status(metric:Gauge, all_containers:list):
    # update the running container_names that is offline with the status of all containers
    # client = docker_env()
    # all_containers = client.containers.list(all=True)
    for container in all_containers:
        if container.name in init_containers_names:
            metric.labels(container_name=container.name).set(1 if container.status == "running" else 0)
        elif container.status == "running":
            metric.labels(container_name=container.name).set(1)
            init_containers_names.append(container.name)
            
    for removed_container_name in init_containers_names:
        if removed_container_name not in [c.name for c in all_containers]:
            metric.labels(container_name=removed_container_name).set(0)