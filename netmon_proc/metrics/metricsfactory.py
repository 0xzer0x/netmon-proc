from netmon_proc.metrics.compositemetric import CompositeMetric
from netmon_proc.metrics.metric import Metric
from netmon_proc.metrics.metrictype import MetricType
from netmon_proc.metrics.rxbytesmetric import RxBytesMetric
from netmon_proc.metrics.txbytesmetric import TxBytesMetric

METRICS_MAP: dict = {"received": RxBytesMetric, "sent": TxBytesMetric}
METRICS_GROUPS: dict = {"transferred": ("received", "sent")}


class MetricsFactory:
    @staticmethod
    def from_name(name: str):
        if name not in METRICS_MAP:
            raise KeyError
        return METRICS_MAP[name]()

    @staticmethod
    def from_list(metrics: list[MetricType]):
        composite: Metric = CompositeMetric("Collected")
        for m in metrics:
            if m in METRICS_MAP:
                composite.add(MetricsFactory.from_name(m))
            elif m in METRICS_GROUPS:
                composite.add(MetricsFactory.from_grp(m))
        return composite
