import signal
from enum import IntEnum

from rich.console import Console
from typing_extensions import Optional
from yaspin import yaspin
from yaspin.core import Yaspin

from netmon_proc.cli.opts import Opts
from netmon_proc.cli.utils import yaspin_terminator
from netmon_proc.patterns.singleton import SingletonMeta

YASPIN_SIGMAP: dict = {
    signal.SIGINT: yaspin_terminator,
    signal.SIGTERM: yaspin_terminator,
}


class LogLevel(IntEnum):
    INFO = 1
    WARN = 2
    ERROR = 3
    SUCCESS = 4


class Logger(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._opts: Opts = Opts()
        self._rich_console: Console = Console()
        self._yaspin: Optional[Yaspin] = None

    def start_spinner(self, *args, **kwargs) -> Optional[Yaspin]:
        if self._opts.silent():
            return None
        self._yaspin = yaspin(*args, **kwargs, sigmap=YASPIN_SIGMAP)
        self._yaspin.start()
        return self._yaspin

    def stop_spinner(self) -> None:
        if self._opts.silent():
            return
        if self._yaspin:
            self._yaspin.hide()
            self._yaspin.stop()
            self._yaspin = None

    def log(self, level: LogLevel, msg: str, extra: bool = False) -> None:
        if self._opts.silent() or (extra and not self._opts.verbose()):
            return

        style: str = ""
        symbol: str = ""
        if level == LogLevel.INFO:
            style = "bold cyan"
            symbol = "+"
        elif level == LogLevel.WARN:
            style = "bold yellow"
            symbol = "!"
        elif level == LogLevel.ERROR:
            style = "bold red"
            symbol = "!"
        elif level == LogLevel.SUCCESS:
            style = "bold green"
            symbol = "$"

        if self._yaspin:
            with self._yaspin.hidden():
                self._rich_console.print(f"[{style}][{symbol}] {msg}[/{style}]")
        else:
            self._rich_console.print(f"[{style}][{symbol}] {msg}[/{style}]")
