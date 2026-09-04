import time

import serial
from serial.tools import list_ports

from syspanel.config import (
    ARDUINO_PID,
    ARDUINO_VID,
    BAUD_RATE,
)


def find_arduino():
    for port in list_ports.comports():
        if port.vid == ARDUINO_VID and port.pid == ARDUINO_PID:
            return port.device

    return None


def connect():
    while True:
        port = find_arduino()

        if port is not None:
            try:
                print(f"Connecting to Arduino on {port}...")

                arduino = serial.Serial(
                    port,
                    BAUD_RATE,
                    timeout=1,
                )

                time.sleep(2)

                print("Connected.")
                return arduino

            except serial.SerialException:
                pass

        print("Arduino not found. Retrying...")
        time.sleep(2)


def send(arduino, message):
    arduino.write(message.encode())


def close(arduino):
    try:
        arduino.close()
    except serial.SerialException:
        pass
