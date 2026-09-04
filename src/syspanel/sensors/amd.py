from pathlib import Path


DRM_PATH = Path("/sys/class/drm")


def find_amd_gpu():
    if not DRM_PATH.exists():
        return None

    for card in DRM_PATH.glob("card[0-9]*"):
        driver = card / "device" / "driver"

        try:
            if driver.resolve().name == "amdgpu":
                return card
        except (FileNotFoundError, OSError):
            continue

    return None


def is_available():
    return find_amd_gpu() is not None


def get_gpu_stats():
    card = find_amd_gpu()

    if card is None:
        return 0, 0

    try:
        hwmon_root = card / "device" / "hwmon"

        hwmon = next(hwmon_root.glob("hwmon*"))

        temp_path = hwmon / "temp1_input"
        usage_path = card / "device" / "gpu_busy_percent"

        temp = int(temp_path.read_text().strip()) / 1000
        usage = int(usage_path.read_text().strip())

        return round(temp), usage

    except (
        FileNotFoundError,
        OSError,
        StopIteration,
        ValueError,
    ):
        return 0, 0
