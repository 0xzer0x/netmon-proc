from psutil import AccessDenied, NoSuchProcess, Process

from netmon_proc.socketwatcher.fetchingexception import FetchingException
from netmon_proc.socketwatcher.fetchingstrategy import FetchingStrategy
from netmon_proc.socketwatcher.socket import Socket


class PsutilFetchingStrategy(FetchingStrategy):
    def fetch(self, pid: int) -> set[Socket]:
        try:
            sockets: set[Socket] = {
                Socket(conn.laddr.port, conn.raddr.port)
                for conn in Process(pid).net_connections()
                if conn.laddr and conn.raddr
            }
        except (AccessDenied, NoSuchProcess) as exc:
            msg: str = (
                "Insufficient permissions"
                if isinstance(exc, AccessDenied)
                else f"Process with PID '{pid}' does not exist"
            )
            raise FetchingException(msg) from exc

        return sockets
