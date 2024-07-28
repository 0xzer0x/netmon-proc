from typing import Optional

from rich.console import Console
from typer import FileTextWrite

from netmon_proc.cli.opts import Opts
from netmon_proc.formatter import MetricsFormatter, MetricsFormatterFactory
from netmon_proc.metrics import Metric


def yaspin_terminator(*_, spinner) -> None:
    spinner.hide()
    spinner.stop()
    raise KeyboardInterrupt


def output_metrics(collected: Metric) -> None:
    console: Console = Console()
    opts: Opts = Opts()
    formatter: MetricsFormatter = MetricsFormatterFactory().get_formatter(
        opts.output_format()
    )

    outfile: Optional[FileTextWrite] = opts.output_file()
    if outfile:
        outfile.write(formatter.format(collected))
    else:
        console.print(formatter.format(collected))
