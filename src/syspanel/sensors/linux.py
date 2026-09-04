import psutil


def get_cpu_temp():
    temps = psutil.sensors_temperatures()

    preferred = (
        ("k10temp", "Tctl"),
        ("coretemp", "Package id 0"),
        ("cpu_thermal", "CPU"),
    )

    for sensor_name, label in preferred:
        for sensor in temps.get(sensor_name, []):
            if sensor.label == label:
                return sensor.current

    return 0


def get_cpu_usage():
    return psutil.cpu_percent()