import platform

from syspanel.sensors.gpu import (
    get_gpu_backend,
    get_gpu_stats,
)


SYSTEM = platform.system()


if SYSTEM == "Linux":
    from syspanel.sensors.linux import (
        get_cpu_temp,
        get_cpu_usage,
    )

elif SYSTEM == "Windows":
    from syspanel.sensors.windows import (
        get_cpu_temp,
        get_cpu_usage,
    )

else:
    def get_cpu_temp():
        return 0


    def get_cpu_usage():
        return 0


__all__ = [
    "get_cpu_temp",
    "get_cpu_usage",
    "get_gpu_backend",
    "get_gpu_stats",
]