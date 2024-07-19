from netmon_proc.metrics.metric import Metric


def is_composite(metric: Metric):
    try:
        metric.value()
        return False
    except NotImplementedError:
        return True


def as_dict(metric: Metric):
    final: dict = {"name": metric.name()}
    if is_composite(metric):
        final["children"] = []
        for child in metric.children():
            final["children"].append(as_dict(child))
    else:
        final["value"] = metric.value()
        final["unit"] = metric.unit()

    return final


def bytes_to_hr(num_bytes: int):
    for unit in ["B", "Ki", "Mi", "Gi", "Ti", "Pi"]:
        if num_bytes < 1024:
            return (f"{num_bytes:.2f}", unit)
        num_bytes /= 1024
    return None
