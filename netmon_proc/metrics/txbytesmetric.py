from scapy.layers.inet import TCP, UDP
from scapy.packet import Packet

from netmon_proc.metrics.leafmetric import LeafMetric
from netmon_proc.netinfo import MAC_ADDRS


class TxBytesMetric(LeafMetric):
    def __init__(self):
        super().__init__("Sent")
        self._unit = "bytes"

    def __iadd__(self, packet: Packet):
        for layer in (TCP, UDP):
            if packet.haslayer(layer) and packet.src in MAC_ADDRS:
                self._value += len(packet[layer].payload)
                break
        return self

    def __add__(self, packet: Packet):
        new_metric = TxBytesMetric()
        for layer in (TCP, UDP):
            if packet.haslayer(layer) and packet.src in MAC_ADDRS:
                new_metric._value = self._value + len(packet[layer].payload)
                break
        return new_metric
