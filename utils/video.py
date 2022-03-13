
from .command import run_command, has_libx265

from typing import List, Optional


def try_use_libx265_video_codec(dst: str):
    x265 = (
        " -c:v libx265"
        if dst.lower().endswith(".mp4") and has_libx265()
        else " -c:v copy")
    return x265


class ClipConfig(object):

    def __init__(self, src_index: int,
                 start: float = 0., end: Optional[float] = None,
                 motion_speed: float = 1., crop: Optional[dict] = None) -> None:
        self.src_index = src_index
        self.start = start
        self.end = end
        self.motion_speed = motion_speed
        self.crop = crop
        if self.crop is not None:
            for k in ["w", "h", "x", "y"]:
                if k not in self.crop:
                    raise KeyError(f"self.crop does not contain key `{k}`")

    def filter_complex_string_for_video(self):
        trim_end = f":{self.end}" if self.end is not None else ""
        crop_spec = (f",crop=w={self.crop.w}:h={self.crop.h}"
                     f":x={self.crop.x}:y={self.crop.y}"
                     if self.crop is not None else "")
        return (
            f"[{self.src_index}:v] "
            f"trim={self.start}{trim_end}"
            f",setpts={1./self.motion_speed}*(PTS-STARTPTS)"
            f"{crop_spec}")

    def filter_complex_string_for_audio(self):
        trim_end = f":{self.end}" if self.end is not None else ""
        return (
            f"[{self.src_index}:a] "
            f"atrim={self.start}{trim_end}"
            f",asetpts=PTS-STARTPTS"
            f",atempo={self.motion_speed}"
        )


def resize(src: str, dst: str, width: int = 1920, height: int = 1080,
           crf: int = 28, preset: str = "fast") -> int:
    cmd = (
        f"ffmpeg -i {src!r}"
        f"{try_use_libx265_video_codec(dst)}"
        f" -crf {crf} -preset {preset}"
        f" -c:a aac"
        f" -s {width}x{height}"
        f" -ignore_unknown"
        f" -y {dst!r}"
    )
    return run_command(cmd)


def concat_video_clips(
    src_seq: List[str],
    clipconfig_seq: List[ClipConfig],
    dst: str
) -> int:
    if len(clipconfig_seq) == 0:
        raise ValueError("clipconfig_seq is Empty.")
    src_string = " ".join(f"-i {src!r}" for src in src_seq)
    filter_complex = ""
    concat_arg = ""
    for i, conf in enumerate(clipconfig_seq):
        filter_complex += f"{conf.filter_complex_string_for_video()} [v{i}]; "
        filter_complex += f"{conf.filter_complex_string_for_audio()} [a{i}]; "
        concat_arg += f"[v{i}][a{i}]"
    concat_arg += f" concat=n={len(clipconfig_seq)}:v=1:a=1 [out]"
    filter_complex += concat_arg
    cmd = (
        f"ffmpeg {src_string}"
        f" -filter_complex {filter_complex!r}"
        f" -map \"[out]\""
        f"{try_use_libx265_video_codec(dst)}"
        f" -y {dst!r}"
    )
    print(cmd)
    return run_command(cmd)
