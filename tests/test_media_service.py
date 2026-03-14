from app.services.media_service import ffmpeg_cut_cmd, ffmpeg_extract_audio_cmd, ffmpeg_merge_cmd, ffmpeg_subtitle_cmd


def test_ffmpeg_commands():
    assert ffmpeg_cut_cmd("in.mp4", "out.mp4", "00:00:01", "00:00:02")[0] == "ffmpeg"
    assert "concat" in ffmpeg_merge_cmd("files.txt", "o.mp4")
    assert "-vn" in ffmpeg_extract_audio_cmd("in.mp4", "a.mp3")
    assert ffmpeg_subtitle_cmd("in.mp4", "s.srt")[-1] == "s.srt"
