from typer import FileTextWrite
from typing_extensions import Optional

from netmon_proc.patterns.singleton import SingletonMeta


class Opts(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._running: bool = True
        self._verbose: bool = False
        self._silent: bool = False
        self._output_format: str = "table"
        self._output_file: Optional[FileTextWrite] = None

    def running(self) -> bool:
        return self._running

    def set_running(self, running: bool) -> None:
        self._running = running

    def verbose(self) -> bool:
        return self._verbose

    def set_verbose(self, verbose: bool) -> None:
        self._verbose = verbose

    def silent(self) -> bool:
        return self._silent

    def set_silent(self, silent: bool) -> None:
        self._silent = silent

    def output_format(self) -> str:
        return self._output_format

    def set_output_format(self, output_format: str) -> None:
        self._output_format = output_format

    def output_file(self) -> Optional[FileTextWrite]:
        return self._output_file

    def set_output_file(self, output_file: Optional[FileTextWrite]) -> None:
        self._output_file = output_file
