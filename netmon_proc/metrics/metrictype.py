from enum import Enum


class MetricType(str, Enum):
    bytes = "bytes"
    rx_bytes = "rx_bytes"
    tx_bytes = "tx_bytes"

    packets = "packets"
    rx_packets = "rx_packets"
    tx_packets = "tx_packets"
