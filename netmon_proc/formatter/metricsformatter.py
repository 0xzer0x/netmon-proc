from abc import ABC, abstractmethod

from netmon_proc.metrics.metric import Metric


class MetricsFormatter(ABC):

    @abstractmethod
    def format(self, metrics: list[Metric]):
        pass
