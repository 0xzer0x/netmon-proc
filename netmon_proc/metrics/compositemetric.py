from scapy.packet import Packet

from netmon_proc.metrics.metric import Metric


class CompositeMetric(Metric):
    def __init__(self, name):
        self._name = name
        self._children: list[Metric] = []

    def __iadd__(self, packet: Packet):
        for metric in self._children:
            metric += packet
        return self

    def __add__(self, packet: Packet):
        new_composite = CompositeMetric(self._name)
        for metric in self._children:
            new_composite.add(metric + packet)
        return new_composite

    def __str__(self):
        result = f"== {self._name} ==\n"
        for metric in self._children:
            result += str(metric) + "\n"
        return result.strip()

    def name(self):
        return self._name

    def add(self, metric: Metric):
        self._children.append(metric)

    def remove(self, metric: Metric):
        self._children.remove(metric)

    def children(self):
        return self._children

    def value(self):
        raise NotImplementedError("Composite nodes don't have a value")

    def unit(self):
        raise NotImplementedError("Composite nodes don't have a unit")
