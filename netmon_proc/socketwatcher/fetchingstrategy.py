from abc import ABC, abstractmethod

from netmon_proc.socketwatcher.socket import Socket


class FetchingStrategy(ABC):
    @abstractmethod
    def fetch(self, pid: int) -> set[Socket]:
        pass
