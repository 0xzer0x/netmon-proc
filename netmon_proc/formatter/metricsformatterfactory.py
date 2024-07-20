from netmon_proc.formatter.jsonmetricsformatter import JsonMetricsFormatter
from netmon_proc.formatter.metricsformatter import MetricsFormatter
from netmon_proc.formatter.tablemetricsformatter import TableMetricsFormatter


class MetricsFormatterFactory:
    @staticmethod
    def get_formatter(format_type: str) -> MetricsFormatter:
        if format_type == "json":
            return JsonMetricsFormatter()
        if format_type == "table":
            return TableMetricsFormatter()
        raise ValueError(f"Unknown format type: {format_type}")
