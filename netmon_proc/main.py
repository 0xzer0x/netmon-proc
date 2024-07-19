import signal
import sys
import time
from threading import Thread
from typing import List

import typer
from rich.console import Console
from typing_extensions import Annotated
from yaspin.spinners import Spinners

import netmon_proc.utils
from netmon_proc.cli import Logger, LogLevel, Opts
from netmon_proc.formatter import JsonMetricsFormatter, MetricsFormatter
from netmon_proc.metrics import Metric, MetricsFactory, MetricType
from netmon_proc.sniffer import PacketSniffer
from netmon_proc.socketwatcher import SocketWatcher

LOGGER: Logger = Logger()
OPTS: Opts = Opts()
COLLECTED: Metric = None


def output_metrics(collected: Metric):
    console: Console = Console()
    formatter: MetricsFormatter = JsonMetricsFormatter()
    console.print_json(formatter.format(collected))


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
        bool, typer.Option("--silent", "-s", help="Show only the collected metrics")
    ] = False,
    bpf_filter: Annotated[
        str, typer.Option("--filter", "-f", help="BPF filter to use")
    ] = "",
    metrics: Annotated[
        List[MetricType], typer.Option("--metrics", "-m", help="Metrics to collect")
    ] = [MetricType.received],
):
    OPTS.set_verbose(verbose)
    OPTS.set_silent(silent)

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

    collected = MetricsFactory.from_list(metrics)

    socketwatcher = SocketWatcher(pids)
    socketwatcher_thread = Thread(target=socketwatcher.start)
    socketwatcher_thread.start()

    sniffer = PacketSniffer(bpf_filter, collected)
    sniffer.start()

    OPTS.set_running(False)
    output_metrics(collected)


def run():
    typer.run(main)
