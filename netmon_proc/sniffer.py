import typer
from scapy.error import Scapy_Exception
from scapy.packet import Packet
from scapy.sendrecv import sniff
from yaspin.spinners import Spinners

from netmon_proc.cli.logger import Logger, LogLevel
from netmon_proc.cli.opts import Opts
from netmon_proc.metrics.metric import Metric
from netmon_proc.socket import Socket
from netmon_proc.socketwatcher import OPEN_SOCKETS


class PacketSniffer:
    def __init__(self, bpf_filter: str, metric: Metric):
        self._bpf_filter: str = bpf_filter
        self._metric: Metric = metric
        self._logger: Logger = Logger()
        self._opts: Opts = Opts()

    def _process_packet(self, packet: Packet):
        try:
            packet_connection = Socket(packet.sport, packet.dport)
        except (AttributeError, IndexError):
            pass
        else:
            if packet_connection in OPEN_SOCKETS:
                try:
                    self._metric += packet
                except TypeError:
                    pass

    def start(self):
        try:
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
                "Insufficient permissions. Root privileges required."
                if isinstance(exc, PermissionError)
                else f"Scapy Error: {exc}"
            )
            self._logger.log(LogLevel.ERROR, errormsg)
            raise typer.Exit(1) from exc
