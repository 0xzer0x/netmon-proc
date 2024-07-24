import typer
from scapy.error import Scapy_Exception
from scapy.layers.inet import IP
from scapy.packet import Packet
from scapy.sendrecv import sniff
from yaspin.spinners import Spinners

from netmon_proc.cli.logger import Logger, LogLevel
from netmon_proc.cli.opts import Opts
from netmon_proc.metrics.metric import Metric
from netmon_proc.socket import Socket
from netmon_proc.socketwatcher import OPEN_SOCKETS, OPEN_SOCKETS_LOCK


class PacketSniffer:
    def __init__(self, bpf_filter: str, metric: Metric):
        self._bpf_filter: str = bpf_filter
        self._metric: Metric = metric
        self._logger: Logger = Logger()
        self._opts: Opts = Opts()

    def _process_packet(self, packet: Packet):
        capture: bool = False
        with OPEN_SOCKETS_LOCK:
            try:
                capture = (
                    Socket(packet.sport, packet.dport) in OPEN_SOCKETS
                    or Socket(packet.dport, packet.sport) in OPEN_SOCKETS
                )
            except (AttributeError, IndexError):
                capture = False

        if capture:
            try:
                self._metric += packet
            except TypeError:
                pass

    def start(self):
        try:
            self._logger.log(
                LogLevel.INFO,
                f"Packet filtering expression: {self._bpf_filter}",
                True,
            )
            self._logger.log(LogLevel.INFO, "Started sniffing packets", True)
            self._logger.start_spinner(
                Spinners.dots,
                text="Monitoring traffic",
                color="blue",
            )
            sniff(
                store=False,
                prn=self._process_packet,
                filter=self._bpf_filter,
            )
            self._logger.stop_spinner()
        except (PermissionError, Scapy_Exception) as exc:
            self._opts.set_running(False)
            self._logger.stop_spinner()
            errormsg: str = (
                "Insufficient permissions to capture traffic. Exiting."
                if isinstance(exc, PermissionError)
                else f"Scapy Error: {exc}"
            )
            self._logger.log(LogLevel.ERROR, errormsg)
            raise typer.Exit(1) from exc
