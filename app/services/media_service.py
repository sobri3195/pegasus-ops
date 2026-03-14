"""Service layer helpers for media processing utilities."""

from __future__ import annotations

import re
from pathlib import Path

TIMESTAMP_RE = re.compile(r"^\d{2}:\d{2}:\d{2}$")


def sanitize_filename(filename: str | None, *, fallback: str = "uploaded.bin") -> str:
    candidate = (filename or "").strip()
    if not candidate:
        return fallback
    safe = re.sub(r"[^A-Za-z0-9._-]", "_", candidate)
    return safe[:120] or fallback


def validate_timestamp(timestamp: str) -> str:
    if not TIMESTAMP_RE.match(timestamp):
        msg = "Timestamp harus berformat HH:MM:SS"
        raise ValueError(msg)

    hh, mm, ss = [int(value) for value in timestamp.split(":")]
    if mm > 59 or ss > 59:
        msg = "Menit dan detik harus berada di rentang 00..59"
        raise ValueError(msg)
    if hh > 23:
        msg = "Jam harus berada di rentang 00..23"
        raise ValueError(msg)
    return timestamp


def validate_dimensions(width: int, height: int) -> tuple[int, int]:
    if width < 16 or height < 16:
        msg = "Dimensi minimum adalah 16x16"
        raise ValueError(msg)
    if width > 7680 or height > 4320:
        msg = "Dimensi melebihi batas maksimum (7680x4320)"
        raise ValueError(msg)
    return width, height


def ensure_parent(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def resize_thumbnail(input_path: Path, output_path: Path, width: int, height: int) -> Path:
    from PIL import Image

    validated_width, validated_height = validate_dimensions(width, height)
    output_path = ensure_parent(output_path)
    with Image.open(input_path) as img:
        resized = img.resize((validated_width, validated_height))
        resized.save(output_path)
    return output_path


def ffmpeg_cut_cmd(input_file: str, output_file: str, start: str, duration: str) -> list[str]:
    return ["ffmpeg", "-y", "-ss", validate_timestamp(start), "-i", input_file, "-t", validate_timestamp(duration), "-c", "copy", output_file]


def ffmpeg_merge_cmd(file_list_path: str, output_file: str) -> list[str]:
    return ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", file_list_path, "-c", "copy", output_file]


def ffmpeg_extract_audio_cmd(input_file: str, output_file: str) -> list[str]:
    return ["ffmpeg", "-y", "-i", input_file, "-vn", "-acodec", "mp3", output_file]


def ffmpeg_subtitle_cmd(input_file: str, output_srt: str) -> list[str]:
    return ["ffmpeg", "-y", "-i", input_file, "-map", "0:s:0?", output_srt]
