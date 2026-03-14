"""Service layer for first 5 real implementations backed by FFmpeg/Pillow."""
from pathlib import Path



def resize_thumbnail(input_path: Path, output_path: Path, width: int, height: int) -> Path:
    from PIL import Image

    with Image.open(input_path) as img:
        resized = img.resize((width, height))
        resized.save(output_path)
    return output_path


def ffmpeg_cut_cmd(input_file: str, output_file: str, start: str, duration: str) -> list[str]:
    return ["ffmpeg", "-y", "-ss", start, "-i", input_file, "-t", duration, "-c", "copy", output_file]


def ffmpeg_merge_cmd(file_list_path: str, output_file: str) -> list[str]:
    return ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path, "-c", "copy", output_file]


def ffmpeg_extract_audio_cmd(input_file: str, output_file: str) -> list[str]:
    return ["ffmpeg", "-y", "-i", input_file, "-vn", "-acodec", "mp3", output_file]


def ffmpeg_subtitle_cmd(input_file: str, output_srt: str) -> list[str]:
    return ["ffmpeg", "-y", "-i", input_file, "-map", "0:s:0?", output_srt]
