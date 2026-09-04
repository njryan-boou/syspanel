from syspanel.sensors import (
    get_cpu_temp,
    get_cpu_usage,
    get_gpu_stats,
)


def get_hardware_stats():
    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()

    gpu_temp, gpu_usage = get_gpu_stats()

    return {
        "cpu_temp": cpu_temp,
        "cpu_usage": cpu_usage,
        "gpu_temp": gpu_temp,
        "gpu_usage": gpu_usage,
    }