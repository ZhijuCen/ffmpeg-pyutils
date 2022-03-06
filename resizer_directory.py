
from utils import resize

import sys
from pathlib import Path
from argparse import ArgumentParser, Namespace


SUPPORTED_EXTS = (".avi", ".mp4", ".mov")


def main(args: Namespace):
    source_dir = Path(args.source_dir)
    destination_dir = Path(args.destination_dir)
    if source_dir == destination_dir:
        print("Video files cannot write inplace.")
        sys.exit()
    if not destination_dir.exists():
        user_input = "NEXT"
        while user_input not in ("", "n", "y"):
            user_input = input(f"Directory `{str(destination_dir)}` does not exists,"
                               f"\nmake new directory[y/N]: ")
            if user_input.lower() == "y":
                destination_dir.mkdir(parents=True, exist_ok=True)
            elif user_input.lower() in ("n", ""):
                sys.exit()

    width = args.width
    height = args.height
    for src_filepath in source_dir.iterdir():
        if src_filepath.is_file() and str(src_filepath).endswith(SUPPORTED_EXTS):
            dst_filepath = destination_dir.joinpath(src_filepath.stem + args.ext)
            ret_code = resize(str(src_filepath), str(dst_filepath), width, height)
            if ret_code != 0:
                print(f"ret_code is not 0 while output file {str(dst_filepath)}.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--source-dir", type=str, required=True,
                        help="Source directory containing video files.")
    parser.add_argument("-d", "--destination-dir", type=str, required=True,
                        help="Destination directory that output video stores at.")
    parser.add_argument("--width", type=int, help="width of output video.")
    parser.add_argument("--height", type=int, help="height of output video.")
    parser.add_argument("--ext", type=str, default=".mp4",
                        help="Extension of output video file. Default: %(default)r")
    args = parser.parse_args()
    main(args)
