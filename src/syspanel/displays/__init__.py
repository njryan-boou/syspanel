from syspanel.config import DISPLAY


def get_renderer():
    if DISPLAY == "lcd2004":
        from syspanel.displays.lcd2004 import render

        return render

    raise ValueError(
        f"Unsupported display: {DISPLAY}"
    )


render = get_renderer()


__all__ = [
    "get_renderer",
    "render",
]