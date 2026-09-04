from pathlib import Path
import tomllib


CONFIG_DIR = Path.home() / ".config" / "syspanel"
CONFIG_FILE = CONFIG_DIR / "config.toml"


DEFAULTS = {
    "display": "lcd2004",
    "transport": "serial",
    "refresh_rate": 1.0,
    "gpu": "auto",
}


# Serial defaults
ARDUINO_VID = 0x2341
ARDUINO_PID = 0x0043
BAUD_RATE = 9600


# LCD defaults
LCD_COLUMNS = 20
LCD_ROWS = 4


def load_config():
    config = DEFAULTS.copy()

    if not CONFIG_FILE.exists():
        return config

    try:
        with CONFIG_FILE.open("rb") as file:
            user_config = tomllib.load(file)

        config.update(user_config)

    except (OSError, tomllib.TOMLDecodeError):
        pass

    return config


def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    contents = (
        f'display = "{config["display"]}"\n'
        f'transport = "{config["transport"]}"\n'
        f'refresh_rate = {config["refresh_rate"]}\n'
        f'gpu = "{config["gpu"]}"\n'
    )

    CONFIG_FILE.write_text(contents)


CONFIG = load_config()

DISPLAY = CONFIG["display"]
TRANSPORT = CONFIG["transport"]
REFRESH_RATE = CONFIG["refresh_rate"]
GPU_BACKEND = CONFIG["gpu"]