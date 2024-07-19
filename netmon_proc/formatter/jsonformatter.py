import json
from io import StringIO

from netmon_proc.formatter.metricsformatter import MetricsFormatter
from netmon_proc.formatter.utils import as_dict
from netmon_proc.metrics.metric import Metric


class JsonMetricsFormatter(MetricsFormatter):
    def format(self, metric: Metric):
        io = StringIO()
        json.dump(as_dict(metric), io)
        return io.getvalue()
