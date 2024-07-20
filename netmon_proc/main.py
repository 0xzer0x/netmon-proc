import signal
import time
from threading import Thread
from typing import List

import typer
from typing_extensions import Annotated
from yaspin.spinners import Spinners

import netmon_proc.utils
from netmon_proc.cli import Logger, LogLevel, Opts
from netmon_proc.cli.utils import output_metrics
from netmon_proc.formatter import Format
from netmon_proc.metrics import MetricFactory, MetricType
from netmon_proc.sniffer import PacketSniffer
from netmon_proc.socketwatcher import SocketWatcher

LOGGER: Logger = Logger()
OPTS: Opts = Opts()

run: typer.Typer = typer.Typer()


@run.command(help="Network traffic monitoring for processes", no_args_is_help=True)
def main(
    processes: Annotated[
        List[str], typer.Argument(help="List of processes to monitor")
    ],
    delay: Annotated[
        float,
        typer.Option(
            "--delay", "-d", min=0, help="Seconds to wait for before monitoring"
        ),
    ] = 0,
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Verbose output")
    ] = False,
    silent: Annotated[
        bool, typer.Option("--silent", "-s", help="Output only the collected metrics")
    ] = False,
    bpf_filter: Annotated[
        str, typer.Option("--filter", "-f", help="Packet filtering expression to apply")
    ] = "",
    metrics: Annotated[
        List[MetricType], typer.Option("--metrics", "-m", help="Metrics to collect")
    ] = [MetricType.rx_bytes],
    output_format: Annotated[
        Format,
        typer.Option(
            "--output-format", "-o", help="Output format for collected metrics"
        ),
    ] = Format.table,
    output_file: Annotated[
        typer.FileTextWrite,
        typer.Option(
            "--output-file",
            "-O",
            help="Write output to file instead of stdout",
            writable=True,
        ),
    ] = None,
):
    OPTS.set_verbose(verbose)
    OPTS.set_silent(silent)
    OPTS.set_output_format(output_format)
    OPTS.set_output_file(output_file)
    collected = MetricFactory.from_list(metrics)

    def signal_handler(*_):
        OPTS.set_running(False)
        if collected is not None:
            output_metrics(collected)
            raise typer.Exit(0)
        raise typer.Exit(1)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if delay > 0:
        LOGGER.start_spinner(
            Spinners.dots, text=f"Waiting for {delay} seconds", color="blue"
        )
        time.sleep(delay)
        LOGGER.stop_spinner()

    pids = netmon_proc.utils.find_pids(processes)
    if len(pids) == 0:
        LOGGER.log(LogLevel.ERROR, "No PID associated with given names")
        raise typer.Exit(1)

    socketwatcher = SocketWatcher(pids)
    socketwatcher_thread = Thread(target=socketwatcher.start)
    socketwatcher_thread.start()

    sniffer = PacketSniffer(bpf_filter, collected)
    sniffer.start()

    OPTS.set_running(False)
    output_metrics(collected)
