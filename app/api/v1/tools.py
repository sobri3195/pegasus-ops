from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.activity import UsageHistory
from app.models.user import User
from app.services.media_service import sanitize_filename, validate_dimensions, validate_timestamp
from app.services.tool_catalog import (
    catalog_summary,
    compare_tools,
    featured_tools,
    filter_tools,
    list_audiences,
    list_categories,
    new_tools,
    paginate_tools,
    random_tools,
    related_tools,
    serialize_tools,
    sort_tools,
    tools_by_audience,
)
from app.tasks.media_tasks import audio_extract, subtitle_generate, thumbnail_resize, video_cut, video_merge

router = APIRouter(prefix="/tools", tags=["tools"])
UPLOAD_DIR = Path(tempfile.gettempdir()) / "pegasus-ops"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _log(db: Session, user: User, slug: str, detail: str):
    db.add(UsageHistory(user_id=user.id, tool_slug=slug, status="queued", detail=detail))
    db.commit()


async def _save_upload(input_file: UploadFile) -> Path:
    filename = sanitize_filename(input_file.filename)
    target = UPLOAD_DIR / filename
    content = await input_file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File upload kosong")
    target.write_bytes(content)
    return target


@router.post("/video-cutter")
async def run_video_cut(
    input_file: UploadFile,
    start: str = Form("00:00:00"),
    duration: str = Form("00:00:10"),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        start = validate_timestamp(start)
        duration = validate_timestamp(duration)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    saved_input = await _save_upload(input_file)
    output = saved_input.with_name(f"cut-{saved_input.name}")
    _log(db, user, "video-cutter", f"start={start},duration={duration},filename={saved_input.name}")
    video_cut.delay(str(saved_input), str(output), start, duration)
    return {"message": "Video cutter job queued", "input": str(saved_input), "output": str(output)}


@router.post("/video-merger")
async def run_video_merge(file_list_path: str = Form(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    _log(db, user, "video-merger", file_list_path)
    video_merge.delay(file_list_path, str(UPLOAD_DIR / "merged-output.mp4"))
    return {"message": "Video merger job queued"}


@router.post("/audio-extractor")
async def run_audio_extract(input_file: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved_input = await _save_upload(input_file)
    output = saved_input.with_suffix(".mp3")
    _log(db, user, "audio-extractor", saved_input.name)
    audio_extract.delay(str(saved_input), str(output))
    return {"message": "Audio extractor job queued", "output": str(output)}


@router.post("/subtitle-generator")
async def run_subtitle(input_file: UploadFile, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    saved_input = await _save_upload(input_file)
    output = saved_input.with_suffix(".srt")
    _log(db, user, "subtitle-generator", saved_input.name)
    subtitle_generate.delay(str(saved_input), str(output))
    return {"message": "Subtitle generator job queued", "output": str(output)}


@router.post("/thumbnail-resizer")
async def run_thumbnail_resize(
    input_file: UploadFile,
    width: int = Form(1280),
    height: int = Form(720),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        width, height = validate_dimensions(width, height)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    saved_input = await _save_upload(input_file)
    output = saved_input.with_name(f"resize-{saved_input.name}")
    _log(db, user, "thumbnail-resizer", f"w={width},h={height},filename={saved_input.name}")
    thumbnail_resize.delay(str(saved_input), str(output), width, height)
    return {"message": "Thumbnail resizer job queued", "output": str(output)}


@router.get("/catalog")
def tool_catalog(
    category: str | None = None,
    query: str | None = None,
    release_stage: str | None = None,
    sort_by: str = "name",
    page: int = 1,
    page_size: int = 10,
):
    filtered = sort_tools(filter_tools(category=category, query=query, release_stage=release_stage), sort_by=sort_by)
    try:
        payload = paginate_tools(filtered, page=page, page_size=page_size)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error

    payload["items"] = serialize_tools(payload["items"])
    payload["categories"] = list_categories()
    payload["audiences"] = list_audiences()
    payload["summary"] = catalog_summary()
    return payload


@router.get("/catalog/featured")
def tool_catalog_featured(limit: int = 6):
    return {"items": serialize_tools(featured_tools(limit=limit)), "limit": limit}


@router.get("/catalog/new")
def tool_catalog_new(limit: int = 10):
    return {"items": serialize_tools(new_tools(limit=limit)), "limit": limit}


@router.get("/catalog/audience/{audience}")
def tool_catalog_by_audience(audience: str, limit: int = 6):
    return {"items": serialize_tools(tools_by_audience(audience, limit=limit)), "audience": audience, "limit": limit}


@router.get("/catalog/random")
def tool_catalog_random(limit: int = 3, seed: int | None = None):
    return {"items": serialize_tools(random_tools(limit=limit, seed=seed)), "limit": limit, "seed": seed}


@router.get("/catalog/compare")
def tool_catalog_compare(slugs: str):
    items = compare_tools(slugs.split(","))
    return {"items": serialize_tools(items), "count": len(items)}


@router.get("/catalog/summary")
def tool_catalog_summary():
    return catalog_summary()


@router.get("/catalog/{slug}/related")
def tool_related(slug: str, limit: int = 4):
    if limit < 1 or limit > 12:
        raise HTTPException(status_code=422, detail="limit harus antara 1 sampai 12")

    items = related_tools(slug, limit=limit)
    if not items:
        raise HTTPException(status_code=404, detail="Tool tidak ditemukan")
    return {"items": serialize_tools(items), "limit": limit}
