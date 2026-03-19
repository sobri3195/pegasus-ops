# Pegasus Ops

**Author: Muhammad Sobri Maulana**

Pegasus Ops adalah aplikasi web fullstack untuk creator, developer, admin, dan tim operasional. Proyek ini menggabungkan katalog tools (60 fitur), dashboard web, autentikasi JWT, logging aktivitas, dan worker async untuk pemrosesan media.

## Dokumentasi
- Tutorial lengkap: [`TUTORIAL.md`](./TUTORIAL.md)
- API + halaman utama: `app/api/v1/`
- Service/business logic: `app/services/`
- Task background: `app/tasks/`

## Stack
- **FastAPI + Jinja2** untuk SSR + API.
- **SQLAlchemy + PostgreSQL** untuk data persistence.
- **Alembic** untuk migrasi.
- **Redis + Celery** untuk background jobs.
- **FFmpeg + Pillow** untuk fitur media.
- **Docker + Nginx** untuk deployment.

## Struktur Proyek
```text
pegasus-ops/
├── app/
│   ├── api/v1/
│   ├── core/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   ├── templates/
│   ├── static/
│   └── main.py
├── alembic/
├── tests/
├── scripts/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── TUTORIAL.md
```

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload
```

Jalankan worker:
```bash
celery -A app.tasks.celery_app.celery worker --loglevel=info
```

## Fitur Utama yang Disempurnakan
1. Validasi upload dan sanitasi nama file pada endpoint tools.
2. Validasi timestamp `HH:MM:SS` dan batas dimensi thumbnail.
3. Normalisasi email saat register/login.
4. Cegah duplikasi email saat registrasi.
5. Utility katalog tools: list, search, grouping by category.

## Katalog 60 Fitur
### Media & Creator
1) Video cutter 2) Video merger 3) Audio extractor 4) Subtitle generator 5) Thumbnail resizer 6) Image compressor 7) Background remover 8) Watermark tool 9) Image format converter 10) Caption generator 11) Hashtag generator 12) Content calendar 13) Bio generator 14) Link in bio builder 15) Reply template manager 16) Engagement tracker 17) Content idea scheduler 18) Title generator 19) Keyword clustering 20) Trend notes board.

### Developer Utilities
21) JSON formatter 22) JWT decoder 23) Base64 encoder/decoder 24) Hash generator 25) Regex tester 26) UUID generator 27) Timestamp converter 28) Color palette generator 29) Markdown previewer 30) API request tester.

### Productivity & Documents
31) To-do board 32) Notes & snippets manager 33) Password generator 34) QR code generator 35) Barcode generator 36) PDF merge 37) PDF split 38) OCR dokumen ringan 39) Invoice template generator 40) Batch file renamer.

### Monitoring & Ops
41) Website uptime checker 42) SSL checker 43) DNS lookup 44) Internal asset port checker 45) Web performance audit 46) Broken link checker 47) Sitemap validator 48) Robots.txt checker 49) Server resource dashboard 50) Log viewer & alert ringan.

### 10 Fitur Baru
51) AI script writer 52) Podcast show notes 53) Email subject generator 54) Schema diff checker 55) Cron expression builder 56) SQL prettifier 57) Meeting recap generator 58) SOP checklist builder 59) Incident timeline tracker 60) Competitor snapshot board.

## Testing
```bash
pytest -q
```
