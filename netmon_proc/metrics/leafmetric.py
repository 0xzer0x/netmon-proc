from abc import abstractmethod

from scapy.packet import Packet

from netmon_proc.metrics.metric import Metric


class LeafMetric(Metric):
    def __init__(self, name):
        self._name: str = name
        self._value: int = 0
        self._unit: str = ""

    def __str__(self):
        return f"{self._name}: {self._value} {self._unit}"

    @abstractmethod
    def __iadd__(self, packet: Packet):
        pass

    @abstractmethod
    def __add__(self, packet: Packet):
        pass

    def name(self):
        return self._name

    def value(self):
        return self._value

    def unit(self):
        return self._unit

    def add(self, metric: Metric):
        raise NotImplementedError("Leaf nodes can't add components")

    def remove(self, metric: Metric):
        raise NotImplementedError("Leaf nodes can't remove components")

    def children(self):
        raise NotImplementedError("Leaf nodes don't have children")
