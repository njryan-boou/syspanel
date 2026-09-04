from syspanel.sensors import (
    get_cpu_temp,
    get_cpu_usage,
    get_gpu_stats,
)


def create_screen():
    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()

    gpu_temp, gpu_usage = get_gpu_stats()

    cpu_temp_text = f"TEMP {cpu_temp:.0f}C"
    gpu_temp_text = f"TEMP {gpu_temp}C"

    cpu_use_text = f"USE {cpu_usage:.0f}%"
    gpu_use_text = f"USE {gpu_usage}%"

    line1 = f"{'CPU':<10}{'GPU':>10}"
    line2 = f"{cpu_temp_text:<10}{gpu_temp_text:>10}"
    line3 = f"{cpu_use_text:<10}{gpu_use_text:>10}"
    line4 = ""

    return (
        f"<"
        f"{line1}\n"
        f"{line2}\n"
        f"{line3}\n"
        f"{line4}"
        f">"
    )
