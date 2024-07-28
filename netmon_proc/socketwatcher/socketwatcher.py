import sys
import time
from threading import Lock

from netmon_proc.cli.logger import Logger, LogLevel
from netmon_proc.cli.opts import Opts
from netmon_proc.socketwatcher.fetchingexception import FetchingException
from netmon_proc.socketwatcher.fetchingstrategy import FetchingStrategy
from netmon_proc.socketwatcher.socket import Socket

OPEN_SOCKETS: set[Socket] = set()
OPEN_SOCKETS_LOCK: Lock = Lock()


class SocketWatcher:
    def __init__(self, pids: set[int], fetching_strategy: FetchingStrategy) -> None:
        self._fetching_strategy: FetchingStrategy = fetching_strategy
        self._pids: set[int] = pids
        self._interval: float = 0.10
        self._opts: Opts = Opts()
        self._logger: Logger = Logger()

    def start(self) -> None:
        while self._opts.running():
            with OPEN_SOCKETS_LOCK:
                OPEN_SOCKETS.clear()
                try:
                    for pid in self._pids:
                        OPEN_SOCKETS.update(self._fetching_strategy.fetch(pid))
                except FetchingException as fex:
                    self._logger.log(
                        LogLevel.ERROR,
                        f"Error during fetching open sockets: {fex.msg}",
                        True,
                    )
                    sys.exit(1)
            self._logger.log(
                LogLevel.WARN,
                f"Open socket: {len(OPEN_SOCKETS)}",
                True,
            )
            time.sleep(self._interval)

    def set_interval(self, interval: float) -> None:
        self._interval = interval

    def interval(self) -> float:
        return self._interval

    def set_pids(self, pids: set[int]) -> None:
        self._pids = pids

    def pids(self) -> set[int]:
        return self._pids
