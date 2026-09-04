import shutil
import subprocess


def is_available():
    return shutil.which("nvidia-smi") is not None


def get_gpu_stats():
    if not is_available():
        return 0, 0

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

        line = result.stdout.strip().splitlines()[0]
        temp, usage = line.split(",")

        return int(temp.strip()), int(usage.strip())

    except (
        IndexError,
        subprocess.SubprocessError,
        ValueError,
    ):
        return 0, 0