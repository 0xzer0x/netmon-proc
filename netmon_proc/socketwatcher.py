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
                for pid in self._pids:
                    proc_sockets = {
                        Socket(conn.laddr.port, conn.raddr.port)
                        for conn in psutil.Process(pid).net_connections()
                        if conn.laddr and conn.raddr
                    }
                    OPEN_SOCKETS.update(proc_sockets)
            self._logger.log(
                LogLevel.WARN,
                f"Open socket: {len(OPEN_SOCKETS)}",
                True,
            )
            # for conn in psutil.net_connections():
            #     if conn.raddr and conn.laddr and conn.pid in self._pids:
            #         old_len = len(OPEN_SOCKETS)
            #         OPEN_SOCKETS.update(
            #             {
            #                 Socket(conn.laddr.port, conn.raddr.port),
            #                 Socket(conn.raddr.port, conn.laddr.port),
            #             }
            #         )
            #         if old_len != len(OPEN_SOCKETS):
            #             self._logger.log(
            #                 LogLevel.WARN,
            #                 f"New socket (lport: {conn.laddr.port}, rport: {conn.raddr.port})",
            #                 True,
            #             )
            time.sleep(self._interval)

    def set_interval(self, interval: float):
        self._interval = interval

    def interval(self):
        return self._interval

    def set_pids(self, pids: set[int]):
        self._pids = pids

    def pids(self):
        return self._pids
