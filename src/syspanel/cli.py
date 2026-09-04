import argparse
import subprocess
import time

import serial

from syspanel.config import (
    CONFIG,
    DISPLAY,
    GPU_BACKEND,
    REFRESH_RATE,
    TRANSPORT,
    save_config,
)
from syspanel.displays import render
from syspanel.monitor import get_hardware_stats
from syspanel.sensors import (
    get_cpu_temp,
    get_cpu_usage,
    get_gpu_backend,
    get_gpu_stats,
)
from syspanel.transports import (
    close,
    connect,
    find_arduino,
    send,
)


SERVICE_NAME = "syspanel.service"


def run_monitor():
    arduino = None

    while True:
        if arduino is None:
            arduino = connect()

        try:
            stats = get_hardware_stats()
            screen = render(stats)

            send(arduino, screen)

            time.sleep(REFRESH_RATE)

        except (serial.SerialException, OSError):
            print("Arduino disconnected.")

            close(arduino)
            arduino = None


def start_service():
    result = subprocess.run(
        ["systemctl", "--user", "start", SERVICE_NAME]
    )

    if result.returncode == 0:
        print("SysPanel started.")


def stop_service():
    result = subprocess.run(
        ["systemctl", "--user", "stop", SERVICE_NAME]
    )

    if result.returncode == 0:
        print("SysPanel stopped.")


def restart_service():
    result = subprocess.run(
        ["systemctl", "--user", "restart", SERVICE_NAME]
    )

    if result.returncode == 0:
        print("SysPanel restarted.")


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
        print("SysPanel: running")
    else:
        print("SysPanel: stopped")

    port = find_arduino()

    print("Display: LCD 20x4")

    if port is None:
        print("Transport: USB Serial (disconnected)")
    else:
        print(f"Transport: USB Serial ({port})")

    cpu_temp = get_cpu_temp()
    cpu_usage = get_cpu_usage()

    gpu_backend = get_gpu_backend()
    gpu_temp, gpu_usage = get_gpu_stats()

    print()
    print(f"CPU: {cpu_temp:.0f}C, {cpu_usage:.0f}%")
    print(
        f"GPU: {gpu_backend.upper()}, "
        f"{gpu_temp}C, {gpu_usage}%"
    )


def show_devices():
    port = find_arduino()

    if port is None:
        print("No SysPanel device detected.")
    else:
        print(f"Arduino: {port}")


def test_display():
    arduino = connect()

    try:
        message = (
            "<"
            "SysPanel Test\n"
            "Display OK\n"
            "Serial OK\n"
            "Ready"
            ">"
        )

        send(arduino, message)

        print("Test message sent.")

    finally:
        close(arduino)


def show_config():
    print("SysPanel configuration")
    print()

    print(f"Display:      {DISPLAY}")
    print(f"Transport:    {TRANSPORT}")
    print(f"Refresh rate: {REFRESH_RATE}s")
    print(f"GPU:          {GPU_BACKEND}")


def set_refresh_rate(value):
    try:
        refresh_rate = float(value)

    except ValueError:
        print("Refresh rate must be a number.")
        return

    if refresh_rate <= 0:
        print("Refresh rate must be greater than 0.")
        return

    config = CONFIG.copy()
    config["refresh_rate"] = refresh_rate

    save_config(config)

    print(f"Refresh rate set to {refresh_rate}s.")
    print("Restart SysPanel to apply the change.")


def main():
    parser = argparse.ArgumentParser(
        prog="syspanel",
        description="PC hardware monitor for external displays",
    )

    subparsers = parser.add_subparsers(
        dest="command",
    )

    subparsers.add_parser(
        "start",
        help="Start SysPanel",
    )

    subparsers.add_parser(
        "stop",
        help="Stop SysPanel",
    )

    subparsers.add_parser(
        "restart",
        help="Restart SysPanel",
    )

    subparsers.add_parser(
        "run",
        help="Run SysPanel in the foreground",
    )

    subparsers.add_parser(
        "status",
        help="Show SysPanel status",
    )

    subparsers.add_parser(
        "devices",
        help="Show detected devices",
    )

    subparsers.add_parser(
        "test",
        help="Send a test message to the display",
    )

    config_parser = subparsers.add_parser(
        "config",
        help="View or change configuration",
    )

    config_parser.add_argument(
        "setting",
        nargs="?",
    )

    config_parser.add_argument(
        "value",
        nargs="?",
    )

    args = parser.parse_args()

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
        if args.setting is None:
            show_config()

        elif args.setting == "refresh":
            if args.value is None:
                print(
                    "Usage: syspanel config "
                    "refresh <seconds>"
                )
            else:
                set_refresh_rate(args.value)

        else:
            print(f"Unknown setting: {args.setting}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()