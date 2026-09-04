import subprocess


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

    except (
        FileNotFoundError,
        subprocess.SubprocessError,
        ValueError,
    ):
        return 0, 0