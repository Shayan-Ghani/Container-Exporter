from asyncio import gather, new_event_loop, wait
from aiodocker import Docker 
from docker import from_env as docker_env
from stats import get_docker_stats as stat
from prometheus_client import Gauge
from prometheus_client.exposition import generate_latest
from flask import Flask, Response, request
from subprocess import run as run_bash
from time import time
from configs import config

app = Flask(__name__)

# Create Prometheus gauge metrics for status and stats
container_status = Gauge('docker_container_status', 'Docker container status (0 = running, 1 = not running)', ['container_name'])
container_cpu_percentage = Gauge('docker_container_cpu_percentage', 'Docker container cpu usage', ['container_name'])
container_memory_percentage =  Gauge('docker_container_memory_percentage', 'Docker container cpu usage', ['container_name'])

def get_container_status(container_names):
    try:
        client = docker_env()
        for container_name in container_names:
          container = client.containers.get(container_name)
          container_status.labels(container_name=container_name).set(0 if container.status == "running" else 1)
        return f"container_status for {container_name} is : {container.status}"
    except Exception as e:
        return f"Error checking container '{container_name}': {str(e)}\n"

# get containers' stats and update their metrics in async mode
async def container_stats():
    start = time()
    docker = Docker()
    containers = await docker.containers.list()
    tasks = [stat.get_container_stats(container) for container in containers]
    all_stats = await gather(*tasks)
    for stats in all_stats:
        # print(stats[0]['name'][1:])
        container_cpu_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_cpu_percentage(stats[0]))
        container_memory_percentage.labels(container_name=stats[0]['name'][1:]).set(stat.calculate_memory_percentage(stats[0]))
    print("container_stats{:10.4f}".format(time() - start), "\n")


@app.route('/')
def index():
    return "Prometheus Exporter for Docker Container Status"

@app.route('/metrics')
def metrics():    
    start = time()
    try:
        # call container_status
        run_bash(["/bin/bash", "./curler.sh"])
        # call container_stats
        loop = new_event_loop()
        t = [loop.create_task(container_stats())]
        loop.run_until_complete(wait(t))
    except Exception as e:
        print(f"Error running script: {str(e)}")
    end = time() - start
    print("metrics{:10.4f}".format(end), "\n")

    # generate the latest value of metrics
    return Response(generate_latest(), mimetype='text/plain')

# get all contianer_names as a list from url arguments and pass them to get_container_status  
@app.route('/check_container')
def check_container():
    container_names = request.args.get('names')
    if container_names:
        container_names_list = container_names.split(',')
        return get_container_status(container_names_list)
    else:
        return "Please provide a container name using the 'name' query parameter."

def create_app():
    app.config.from_object(config.Config)
    return app