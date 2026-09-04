import psutil


def get_cpu_usage():
    return psutil.cpu_percent()


def get_cpu_temp():
    return 0