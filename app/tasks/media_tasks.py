import subprocess
from pathlib import Path

from app.services.media_service import (
    ffmpeg_cut_cmd,
    ffmpeg_extract_audio_cmd,
    ffmpeg_merge_cmd,
    ffmpeg_subtitle_cmd,
    resize_thumbnail,
)
from app.tasks.celery_app import celery_app


@celery_app.task(name="app.tasks.media_tasks.video_cut")
def video_cut(input_file: str, output_file: str, start: str, duration: str):
    subprocess.run(ffmpeg_cut_cmd(input_file, output_file, start, duration), check=True)
    return output_file


@celery_app.task(name="app.tasks.media_tasks.video_merge")
def video_merge(file_list: str, output_file: str):
    subprocess.run(ffmpeg_merge_cmd(file_list, output_file), check=True)
    return output_file


@celery_app.task(name="app.tasks.media_tasks.audio_extract")
def audio_extract(input_file: str, output_file: str):
    subprocess.run(ffmpeg_extract_audio_cmd(input_file, output_file), check=True)
    return output_file


@celery_app.task(name="app.tasks.media_tasks.subtitle_generate")
def subtitle_generate(input_file: str, output_file: str):
    subprocess.run(ffmpeg_subtitle_cmd(input_file, output_file), check=True)
    return output_file


@celery_app.task(name="app.tasks.media_tasks.thumbnail_resize")
def thumbnail_resize(input_file: str, output_file: str, width: int, height: int):
    resize_thumbnail(Path(input_file), Path(output_file), width, height)
    return output_file
