from aiodocker.containers import DockerContainer
from typing import Union, Iterable
from prometheus_client import Gauge, Counter

PromMetric = Union[Gauge, Counter]

def prune_stale_metrics(active_names: Iterable[str], prunable_metrics: list[PromMetric], persistent_metrics : list[PromMetric]):
    """
    Removes time series for inactive containers from selected metrics
    while preserving container status metrics by setting them to 0.
    """
    active_set = set(active_names)

    for metric in prunable_metrics:
        for labels in metric._metrics:
            name = labels[0]
            if name not in active_set:
                metric.clear()
    
    for metric in persistent_metrics:
        for labels in list(metric._metrics):
            name = labels[0]
            if name not in active_set:
                metric.labels(container_name=name).set(0)


def flush_metric_labels(containers:list[DockerContainer], metrics_to_clear: list[PromMetric]):
    for container in containers:
        if container._container.get("State") != "running":
            for metric in metrics_to_clear:
                metric.labels(container_name=container._container.get("Names")[0][1:]).set(0)