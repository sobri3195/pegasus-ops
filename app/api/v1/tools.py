from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.activity import UsageHistory
from app.models.user import User
from app.tasks.media_tasks import audio_extract, subtitle_generate, thumbnail_resize, video_cut, video_merge

router = APIRouter(prefix="/tools", tags=["tools"])


def _log(db: Session, user: User, slug: str, detail: str):
    db.add(UsageHistory(user_id=user.id, tool_slug=slug, status="queued", detail=detail))
    db.commit()


@router.post("/video-cutter")
async def run_video_cut(
    input_file: UploadFile,
    start: str = Form("00:00:00"),
    duration: str = Form("00:00:10"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _log(db, user, "video-cutter", f"start={start},duration={duration},filename={input_file.filename}")
    video_cut.delay(f"/tmp/{input_file.filename}", f"/tmp/cut-{input_file.filename}", start, duration)
    return {"message": "Video cutter job queued"}


@router.post("/video-merger")
async def run_video_merge(file_list_path: str = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _log(db, user, "video-merger", file_list_path)
    video_merge.delay(file_list_path, "/tmp/merged-output.mp4")
    return {"message": "Video merger job queued"}


@router.post("/audio-extractor")
async def run_audio_extract(input_file: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _log(db, user, "audio-extractor", input_file.filename or "")
    audio_extract.delay(f"/tmp/{input_file.filename}", f"/tmp/{input_file.filename}.mp3")
    return {"message": "Audio extractor job queued"}


@router.post("/subtitle-generator")
async def run_subtitle(input_file: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _log(db, user, "subtitle-generator", input_file.filename or "")
    subtitle_generate.delay(f"/tmp/{input_file.filename}", f"/tmp/{input_file.filename}.srt")
    return {"message": "Subtitle generator job queued"}


@router.post("/thumbnail-resizer")
async def run_thumbnail_resize(
    input_file: UploadFile,
    width: int = Form(1280),
    height: int = Form(720),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _log(db, user, "thumbnail-resizer", f"w={width},h={height},filename={input_file.filename}")
    thumbnail_resize.delay(f"/tmp/{input_file.filename}", f"/tmp/resize-{input_file.filename}", width, height)
    return {"message": "Thumbnail resizer job queued"}
