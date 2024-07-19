from abc import ABC, abstractmethod

from scapy.packet import Packet


class Metric(ABC):

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, packet: Packet):
        pass

    @abstractmethod
    def __iadd__(self, packet: Packet):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def value(self):
        pass

    @abstractmethod
    def unit(self):
        pass

    @abstractmethod
    def add(self, metric: "Metric"):
        pass

    @abstractmethod
    def remove(self, metric: "Metric"):
        pass

    @abstractmethod
    def children(self):
        pass
