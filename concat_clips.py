
from utils import concat_video_clips
from utils.video import ClipConfig

from argparse import ArgumentParser
from typing import List
import sys


def pts_to_sec(string: str) -> float:
    time_strings = string.split(":")
    times_multiple = (1, 60, 60, 24)
    sec = 0.
    for i, (v, t) in enumerate(zip(reversed(time_strings), times_multiple)):
        if i == 0:
            sec += float(v) * t
        else:
            sec += int(v) * t
    return sec


def split_by_semicolon(string: str) -> list:
    return string.split(";")


def parse_crop_spec(string: str) -> dict:
    values = string.split(":")
    if len(values) != 4:
        raise ValueError("Number of arg for crop not match, expected in `w:h:x:y` format.")
    values = tuple(int(s) for s in values)
    crop = dict()
    crop["w"], crop["h"], crop["x"], crop["y"] = values
    return crop


def parse_clip_configs(string: str) -> List[ClipConfig]:
    cfg_strings = split_by_semicolon(string)
    if len(cfg_strings) < 2:
        raise ValueError("Configurations for clips must have atleast 2.")
    cfgs = list()
    for clip_spec in cfg_strings:
        args: list = clip_spec.split(",")
        if len(args) == 5:
            args[4] = parse_crop_spec(args[4])
        if len(args) >= 4:
            args[3] = float(args[3])
        if len(args) >= 3:
            if args[2] is not None:
                args[2] = pts_to_sec(args[2])
        if len(args) >= 2:
            args[1] = pts_to_sec(args[1])
        if len(args) >= 1:
            args[0] = int(args[0])
        if len(args) == 0:
            raise ValueError("Each Configuration for clip must have atleast 1 argument.")
        cfgs.append(ClipConfig(*args))
    return cfgs


def main(args):
    return concat_video_clips(args.src, args.clip_configs, args.dst)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "-s", "--src",
        type=split_by_semicolon, required=True,
        help="Paths to source videos spitted by `;`, arg value must be quoted by \' or \".")
    parser.add_argument(
        "-d", "--dst",
        type=str, required=True,
        help="Path to destination video."
    )
    parser.add_argument(
        "-c", "--clip-configs",
        type=parse_clip_configs, required=True,
        help="Configuration for clips to concatenate, each configuration splitted by `;`, args splitted by `,`."
    )
    args = parser.parse_args()
    ret_val = main(args)
    sys.exit(ret_val)
