from rich.console import Console

from netmon_proc.cli.opts import Opts
from netmon_proc.formatter import MetricsFormatter, MetricsFormatterFactory
from netmon_proc.metrics import Metric


def yaspin_terminator(*_, spinner):
    spinner.hide()
    spinner.stop()
    raise KeyboardInterrupt


def output_metrics(collected: Metric):
    console: Console = Console()
    opts: Opts = Opts()
    formatter: MetricsFormatter = MetricsFormatterFactory().get_formatter(
        opts.output_format()
    )

    if opts.output_file() is not None:
        opts.output_file().write(formatter.format(collected))
    else:
        console.print(formatter.format(collected))
