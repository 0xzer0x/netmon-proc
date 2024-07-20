from netmon_proc.patterns.singleton import SingletonMeta


class Opts(metaclass=SingletonMeta):
    def __init__(self):
        self._running = True
        self._verbose = False
        self._silent = False
        self._output_format = "table"

    def running(self):
        return self._running

    def set_running(self, running: bool):
        self._running = running

    def verbose(self):
        return self._verbose

    def set_verbose(self, verbose: bool):
        self._verbose = verbose

    def silent(self):
        return self._silent

    def set_silent(self, silent: bool):
        self._silent = silent

    def output_format(self):
        return self._output_format

    def set_output_format(self, output_format: str):
        self._output_format = output_format
