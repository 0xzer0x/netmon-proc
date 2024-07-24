import sys
import time
from threading import Lock

import psutil

from netmon_proc.cli.logger import Logger, LogLevel
from netmon_proc.cli.opts import Opts
from netmon_proc.socket import Socket

OPEN_SOCKETS: set[Socket] = set()
OPEN_SOCKETS_LOCK: Lock = Lock()


class SocketWatcher:
    def __init__(self, pids: set[int]):
        self._pids: set[int] = pids
        self._interval: float = 0.10
        self._opts: Opts = Opts()
        self._logger: Logger = Logger()

    def start(self):
        while self._opts.running():
            with OPEN_SOCKETS_LOCK:
                OPEN_SOCKETS.clear()
                try:
                    for pid in self._pids:
                        proc_sockets = {
                            Socket(conn.laddr.port, conn.raddr.port)
                            for conn in psutil.Process(pid).net_connections()
                            if conn.laddr and conn.raddr
                        }
                        OPEN_SOCKETS.update(proc_sockets)
                except psutil.AccessDenied as exc:
                    self._logger.log(
                        LogLevel.ERROR,
                        "Insufficent permissions to read process connections. Exiting.",
                        True,
                    )
                    sys.exit(1)
            self._logger.log(
                LogLevel.WARN,
                f"Open socket: {len(OPEN_SOCKETS)}",
                True,
            )
            time.sleep(self._interval)

    def set_interval(self, interval: float):
        self._interval = interval

    def interval(self):
        return self._interval

    def set_pids(self, pids: set[int]):
        self._pids = pids

    def pids(self):
        return self._pids
