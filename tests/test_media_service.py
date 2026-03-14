import pytest

from app.services.media_service import (
    ffmpeg_cut_cmd,
    ffmpeg_extract_audio_cmd,
    ffmpeg_merge_cmd,
    ffmpeg_subtitle_cmd,
    sanitize_filename,
    validate_dimensions,
    validate_timestamp,
)


def test_ffmpeg_commands():
    assert ffmpeg_cut_cmd("in.mp4", "out.mp4", "00:00:01", "00:00:02")[0] == "ffmpeg"
    assert "concat" in ffmpeg_merge_cmd("files.txt", "o.mp4")
    assert "-vn" in ffmpeg_extract_audio_cmd("in.mp4", "a.mp3")
    assert ffmpeg_subtitle_cmd("in.mp4", "s.srt")[-1] == "s.srt"


def test_sanitize_filename_and_timestamp_validation():
    assert sanitize_filename("../../hack.mp4") == ".._.._hack.mp4"
    assert validate_timestamp("00:00:59") == "00:00:59"

    with pytest.raises(ValueError):
        validate_timestamp("00:61:00")


def test_dimensions_validation():
    assert validate_dimensions(1280, 720) == (1280, 720)
    with pytest.raises(ValueError):
        validate_dimensions(2, 2)
