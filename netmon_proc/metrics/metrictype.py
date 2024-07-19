from enum import Enum


class MetricType(str, Enum):
    transferred = "transferred"
    received = "received"
    sent = "sent"
