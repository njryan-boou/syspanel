from syspanel.sensors.linux import (
    get_cpu_temp,
    get_cpu_usage,
)
from syspanel.sensors.nvidia import get_gpu_stats


__all__ = [
    "get_cpu_temp",
    "get_cpu_usage",
    "get_gpu_stats",
]