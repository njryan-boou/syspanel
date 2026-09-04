import argparse
import subprocess
import time

import serial

from syspanel.config import (
    ARDUINO_PID,
    ARDUINO_VID,
    BAUD_RATE,
    GPU_BACKEND,
    LCD_COLUMNS,
    LCD_ROWS,
    REFRESH_RATE,
)
from syspanel.monitor import create_screen
from syspanel.serial_display import (
    close,
    connect,
    find_arduino,
    send,
)
from syspanel.sensors import (
    get_cpu_temp,
    get_cpu_usage,
    get_gpu_stats,
)


SERVICE_NAME = "syspanel.service"


def run_monitor():
    arduino = None

    while True:
        if arduino is None:
            arduino = connect()

        try:
            screen = create_screen()
            send(arduino, screen)

            time.sleep(REFRESH_RATE)

        except (serial.SerialException, OSError):
            print("Arduino disconnected.")

            close(arduino)
            arduino = None


def start_service():
    result = subprocess.run(
        [
            "systemctl",
            "--user",
            "start",
            SERVICE_NAME,
        ]
    )

    if result.returncode == 0:
        print("syspanel started.")


def stop_service():
    result = subprocess.run(
        [
            "systemctl",
            "--user",
            "stop",
            SERVICE_NAME,
        ]
    )

    if result.returncode == 0:
        print("syspanel stopped.")


def restart_service():
    result = subprocess.run(
        [
            "systemctl",
            "--user",
            "restart",
            SERVICE_NAME,
        ]
    )

    if result.returncode == 0:
        print("syspanel restarted.")


def show_status():
    result = subprocess.run(
        [
            "systemctl",
            "--user",
            "is-active",
            SERVICE_NAME,
        ],
        capture_output=True,
        text=True,
    )

    service_status = result.stdout.strip()

    if service_status == "active":
        print("syspanel: running")
    else:
        print("syspanel: stopped")

    port = find_arduino()

    if port is None:
        print("Display: disconnected")
    else:
        print(f"Display: connected ({port})")

    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()

    gpu_temp, gpu_usage = get_gpu_stats()

    print()
    print(f"CPU: {cpu_temp:.0f}C, {cpu_usage:.0f}%")
    print(f"GPU: {gpu_temp}C, {gpu_usage}%")


def show_devices():
    port = find_arduino()

    if port is None:
        print("No supported displays found.")
        return

    print(f"Arduino LCD: {port}")


def test_display():
    port = find_arduino()

    if port is None:
        print("Arduino LCD not found.")
        return

    arduino = connect()

    try:
        message = (
            "<"
            "SYPANEL TEST         \n"
            "Display connected   \n"
            "Serial working      \n"
            "Test successful     "
            ">"
        )

        send(arduino, message)

        print("Test screen sent.")

    finally:
        close(arduino)


def show_config():
    print("syspanel configuration")
    print()

    print(f"Display:      {LCD_COLUMNS}x{LCD_ROWS}")
    print(f"Refresh rate: {REFRESH_RATE}s")
    print(f"GPU backend:  {GPU_BACKEND}")
    print(f"Baud rate:    {BAUD_RATE}")
    print(f"Arduino VID:  {ARDUINO_VID:#06x}")
    print(f"Arduino PID:  {ARDUINO_PID:#06x}")


def main():
    parser = argparse.ArgumentParser(
        prog="syspanel",
        description="External PC hardware monitor",
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    subparsers.add_parser(
        "start",
        help="Start syspanel in the background",
    )

    subparsers.add_parser(
        "stop",
        help="Stop the background syspanel service",
    )

    subparsers.add_parser(
        "restart",
        help="Restart the background syspanel service",
    )

    subparsers.add_parser(
        "run",
        help="Run syspanel in the foreground",
    )

    subparsers.add_parser(
        "status",
        help="Show hardware and display status",
    )

    subparsers.add_parser(
        "devices",
        help="List connected displays",
    )

    subparsers.add_parser(
        "test",
        help="Send a test screen to the display",
    )

    subparsers.add_parser(
        "config",
        help="Show syspanel configuration",
    )

    args = parser.parse_args()

    try:
        if args.command == "start":
            start_service()

        elif args.command == "stop":
            stop_service()

        elif args.command == "restart":
            restart_service()

        elif args.command == "run":
            run_monitor()

        elif args.command == "status":
            show_status()

        elif args.command == "devices":
            show_devices()

        elif args.command == "test":
            test_display()

        elif args.command == "config":
            show_config()

        else:
            parser.print_help()

    except KeyboardInterrupt:
        print("\nsyspanel stopped.")


if __name__ == "__main__":
    main()