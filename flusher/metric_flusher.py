def flush_metrics(metrics:list, containers):
    for container in containers:
        if container.status != "running":
            for m in metrics:
                m.clear()