from syspanel.sensors import amd
from syspanel.sensors import nvidia


def get_gpu_backend():
    if nvidia.is_available():
        return "nvidia"

    if amd.is_available():
        return "amd"

    return "unsupported"


def get_gpu_stats():
    backend = get_gpu_backend()

    if backend == "nvidia":
        return nvidia.get_gpu_stats()

    if backend == "amd":
        return amd.get_gpu_stats()

    return 0, 0