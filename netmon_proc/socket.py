class Socket:
    def __init__(self, src_port: int, dst_port: int) -> None:
        self._src_port: int = src_port
        self._dst_port: int = dst_port

    def __str__(self) -> str:
        return f"(src: {self._src_port}, dst: {self._dst_port})"

    def __hash__(self) -> int:
        return hash((self._src_port, self._dst_port))

    def __eq__(self, o) -> bool:
        if not isinstance(o, Socket):
            return False
        return o._src_port == self._src_port and o._dst_port == self._dst_port

    def src_port(self) -> str:
        return self._src_port

    def dst_port(self) -> str:
        return self._dst_port
