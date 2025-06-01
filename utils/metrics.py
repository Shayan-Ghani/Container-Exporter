from aiodocker.containers import DockerContainer
from typing import Union, Iterable
from prometheus_client import Gauge, Counter
from settings.settings import settings
PromMetric = Union[Gauge, Counter]

def prune_stale_metrics(active_names: Iterable[str], prunable_metrics: list[PromMetric], persistent_metrics : list[Gauge]):
    """
    Removes time series for inactive containers from selected metrics
    while preserving container status metrics by setting them to 0.
    when CONTAINER_EXPORTER_CLEAR_METRICS is set False it only clears Counter metrics
    Gauge metrics are set to 0.
    """
    active_set = set(active_names)

    for metric in prunable_metrics:
        if not hasattr(metric, '_metrics'):
            continue
        for labels in metric._metrics:
            name = labels[0]
            if name not in active_set:
                if settings.CONTAINER_EXPORTER_CLEAR_METRICS:
                    metric.clear()                    
                elif isinstance(metric, Gauge):
                    metric.labels(container_name=name).set(0)
                else:
                    metric.clear()                    
                        
    for metric in persistent_metrics:
        if not hasattr(metric, '_metrics'):
            continue
        for labels in list(metric._metrics):
            name = labels[0]
            if name not in active_set:
                metric.labels(container_name=name).set(0)

def normalize_name(raw_names: list[str], fallback_id: str) -> str:
    """
    Given Docker’s 'Names' array (e.g. ['/my‐container']), pick the first one and strip leading '/'.
    If it’s missing or empty, return a short version of container ID.
    """
    if raw_names and isinstance(raw_names, list) and raw_names[0]:
        return raw_names[0].lstrip("/")
    return fallback_id[:12]
