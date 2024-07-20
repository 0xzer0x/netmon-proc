from tabulate import tabulate

from netmon_proc.formatter.metricsformatter import MetricsFormatter
from netmon_proc.formatter.utils import as_dict, bytes_to_hr
from netmon_proc.metrics import Metric


class TableMetricsFormatter(MetricsFormatter):
    def _flatten(self, metrics_dict: dict, parent_name: str = ""):
        flattened = []
        name = metrics_dict.get("name", "")
        full_name = f"{parent_name}/{name}" if parent_name else name

        if "children" in metrics_dict:
            for child in metrics_dict["children"]:
                flattened.extend(self._flatten(child, full_name))
        else:
            value, unit = metrics_dict["value"], metrics_dict["unit"]
            if unit == "bytes":
                value, unit = bytes_to_hr(value)
            flattened.append({"name": full_name, "value": value, "unit": unit})

        return flattened

    def format(self, metric: Metric):
        metrics_dict = as_dict(metric)
        table = tabulate(self._flatten(metrics_dict), headers="keys", tablefmt="grid")
        return table
