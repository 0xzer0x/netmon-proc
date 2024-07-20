from netmon_proc.metrics.compositemetric import CompositeMetric
from netmon_proc.metrics.metric import Metric
from netmon_proc.metrics.metrictype import MetricType
from netmon_proc.metrics.rxbytesmetric import RxBytesMetric
from netmon_proc.metrics.rxpacketsmetric import RxPacketsMetric
from netmon_proc.metrics.txbytesmetric import TxBytesMetric
from netmon_proc.metrics.txpacketsmetric import TxPacketsMetric

METRICS_MAP: dict = {
    MetricType.rx_bytes.value: RxBytesMetric,
    MetricType.tx_bytes.value: TxBytesMetric,
    MetricType.rx_packets.value: RxPacketsMetric,
    MetricType.tx_packets.value: TxPacketsMetric,
}


class MetricFactory:
    @staticmethod
    def from_name(name: str):
        if name not in METRICS_MAP:
            raise KeyError
        return METRICS_MAP[name]()

    @staticmethod
    def from_grp(name: str):
        children = [METRICS_MAP[m] for m in METRICS_MAP if m.split("_")[1] == name]
        if len(children) == 0:
            raise KeyError

        composite: Metric = CompositeMetric(name.capitalize())
        for component in children:
            composite.add(component())
        return composite

    @staticmethod
    def from_list(metrics: list[MetricType]):
        composite: Metric = CompositeMetric("Collected")
        for m in metrics:
            if m in METRICS_MAP:
                composite.add(MetricFactory.from_name(m.value))
            else:
                composite.add(MetricFactory.from_grp(m.value))
        return composite
