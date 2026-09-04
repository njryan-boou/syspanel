import time
import subprocess

import psutil
import serial
from serial.tools import list_ports


def find_arduino():
    for port in list_ports.comports():
        if port.vid == 0x2341 and port.pid == 0x0043:
            return port.device

    return None


def connect_arduino():
    while True:
        port = find_arduino()

        if port is not None:
            try:
                print(f"Connecting to Arduino on {port}...")

                arduino = serial.Serial(port, 9600, timeout=1)

                # Arduino resets when the serial connection opens.
                time.sleep(2)

                print("Connected.")
                return arduino

            except serial.SerialException:
                pass

        print("Arduino not found. Retrying...")
        time.sleep(2)


def get_cpu_temp():
    temps = psutil.sensors_temperatures()

    for sensor in temps.get("k10temp", []):
        if sensor.label == "Tctl":
            return sensor.current

    return 0


def get_gpu_stats():
    try:
        result = subprocess.run(
            [
                "nvidia-smi",
                "--query-gpu=temperature.gpu,utilization.gpu",
                "--format=csv,noheader,nounits",
            ],
            capture_output=True,
            text=True,
            timeout=2,
        )

        if result.returncode != 0:
            return 0, 0

        temp, usage = result.stdout.strip().split(",")

        return int(temp), int(usage)

    except (subprocess.SubprocessError, ValueError):
        return 0, 0


def create_screen():
    cpu_temp = get_cpu_temp()
    cpu_usage = psutil.cpu_percent()

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


def main():
    arduino = None

    while True:
        if arduino is None:
            arduino = connect_arduino()

        try:
            message = create_screen()

            arduino.write(message.encode())

            time.sleep(1)

        except (serial.SerialException, OSError):
            print("Arduino disconnected.")

            try:
                arduino.close()
            except Exception:
                pass

            arduino = None


if __name__ == "__main__":
    main()
