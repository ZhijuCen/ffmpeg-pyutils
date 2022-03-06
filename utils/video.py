
from .command import run_command


def resize(src: str, dst: str, width: int = 1280, height: int = 720) -> int:
    x265 = " -c:v libx265" if dst.lower().endswith(".mp4") else " -c:v copy"
    cmd = (f"ffmpeg -i {src!r}"
           f"{x265}"
           f" -crf 28 -preset fast"
           f" -c:a aac"
           f" -s {width}x{height}"
           f" -ignore_unknown"
           f" -y {dst!r}")
    return run_command(cmd)

