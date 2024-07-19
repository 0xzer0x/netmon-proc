import psutil

from netmon_proc.cli.logger import Logger, LogLevel


def find_pids(processes: list[str]) -> set[int]:
    pids: set[int] = set()
    logger: Logger = Logger()

    logger.log(LogLevel.INFO, "Looking for pids of processes", True)
    for p in psutil.process_iter(attrs=["pid", "name"]):
        if p.info["name"] in processes:
            pids.add(p.info["pid"])
            logger.log(
                LogLevel.SUCCESS,
                f"Found process '{p.info['name']}' with pid {p.info['pid']}",
                True,
            )

    return pids
