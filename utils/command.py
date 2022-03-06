
import shlex
import subprocess as sp


def run_command(cmd: str) -> int:
    return sp.run(shlex.split(cmd)).returncode

