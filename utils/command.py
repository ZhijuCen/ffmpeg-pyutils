
import shlex
import subprocess as sp


def run_command(cmd: str) -> int:
    return sp.run(shlex.split(cmd)).returncode


def has_libx265() -> bool:
    return str(sp.run(shlex.split("ffmpeg -codecs"), capture_output=True).stdout, encoding="utf-8").find("libx265") != -1
