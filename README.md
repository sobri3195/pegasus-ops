# Pegasus Ops

**Author: Muhammad Sobri Maulana**

Pegasus Ops adalah aplikasi web fullstack modern untuk creator, developer, admin, dan tim operasional. Platform ini menyatukan media tools, developer utilities, monitoring, document tools, automation, dan productivity tools dalam dashboard profesional yang aman dan scalable.

## 1. Ringkasan Proyek
Pegasus Ops dibangun dengan FastAPI + Jinja2 (server-rendered UI), PostgreSQL, SQLAlchemy, Alembic, Redis, Celery, dan Docker. Arsitektur modular dipisah per domain (`api`, `services`, `models`, `tasks`) agar mudah dikembangkan ke 50+ tools legal dan aman.

## 2. Struktur Folder
```text
pegasus-ops/
├── app/
│   ├── api/v1/           # API routes + page routes
│   ├── core/             # Config, DB, security, deps
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic/tool services
│   ├── tasks/            # Celery app + async workers
│   ├── utils/            # Shared helpers
│   ├── templates/        # Jinja2 UI templates
│   ├── static/           # CSS/JS assets
│   └── main.py
├── alembic/
├── tests/
├── scripts/seed_data.py
├── docker-compose.yml
├── Dockerfile
├── nginx/default.conf
├── requirements.txt
├── .env.example
└── README.md
```

## 3. Penjelasan Stack dan Alasan Pemilihan
- **FastAPI**: cepat, typing kuat, ideal untuk API + SSR backend.
- **Jinja2 + Tailwind CDN**: UI modern server-rendered, performa baik, sederhana.
- **PostgreSQL + SQLAlchemy**: relasional kuat, siap scaling dan audit logging.
- **Alembic**: migrasi schema terkontrol.
- **JWT (cookie)**: auth stateless namun tetap nyaman di web app.
- **Celery + Redis**: background job untuk proses berat media/PDF/OCR.
- **FFmpeg, Pillow, PyMuPDF, Tesseract**: utilitas file processing legal.
- **Docker + Compose + Nginx**: deployment konsisten production-ready.
- **Pytest**: dasar quality gate.

## 4. Daftar 50 Fitur (Kategori)
### Media & Creator
1) Video cutter 2) Video merger 3) Audio extractor 4) Subtitle generator 5) Thumbnail resizer 6) Image compressor 7) Background remover 8) Watermark tool 9) Image format converter 10) Caption generator 11) Hashtag generator 12) Content calendar 13) Bio generator 14) Link in bio builder 15) Reply template manager 16) Engagement tracker 17) Content idea scheduler 18) Title generator 19) Keyword clustering 20) Trend notes board.

### Developer Utilities
21) JSON formatter 22) JWT decoder 23) Base64 encoder/decoder 24) Hash generator 25) Regex tester 26) UUID generator 27) Timestamp converter 28) Color palette generator 29) Markdown previewer 30) API request tester.

### Productivity & Documents
31) To-do board 32) Notes & snippets manager 33) Password generator 34) QR code generator 35) Barcode generator 36) PDF merge 37) PDF split 38) OCR dokumen ringan 39) Invoice template generator 40) Batch file renamer.

### Monitoring & Ops
41) Website uptime checker 42) SSL checker 43) DNS lookup 44) Internal asset port checker (hanya aset milik sendiri) 45) Web performance audit 46) Broken link checker 47) Sitemap validator 48) Robots.txt checker 49) Server resource dashboard 50) Log viewer & alert ringan.

## 5. Desain Database
Tabel inti:
- `users` (akun + role)
- `tools` (master tools)
- `usage_history` (riwayat eksekusi tool)
- `favorite_tools` (pin favorit)
- `audit_logs` (admin audit trail)

Ekstensi berikutnya: `notifications`, `projects`, `teams`, `api_keys`, `system_metrics`.

## 6. Arsitektur Backend
- **Router Layer** (`app/api/v1`): HTTP endpoint, validasi request, response template/JSON.
- **Service Layer** (`app/services`): bisnis logic reusable.
- **Task Layer** (`app/tasks`): Celery async jobs.
- **Data Layer** (`app/models`, `app/schemas`, `app/core/database.py`).
- **Security Layer** (`app/core/security.py`, `app/core/deps.py`) untuk JWT + RBAC.

## 7. Arsitektur Frontend / Template System
- `base.html` sebagai reusable layout.
- Partial reusable: `partials/sidebar.html`, `partials/topbar.html`.
- Halaman utama: landing, login/register, dashboard, settings.
- Gaya: dark futuristic + neon accent + card-based dashboard responsive.

## 8. Authentication & RBAC
- Register/login dengan hash bcrypt.
- JWT disimpan di HTTP-only cookie.
- Dependency `get_current_user` + `require_role({...})` untuk route protection.
- Role awal: `admin`, `operator`, `member`.

## 9. Implementasi 5 Fitur Pertama (Working Example)
- Video cutter (`/api/v1/tools/video-cutter`) → Celery task `video_cut` + FFmpeg command.
- Video merger (`/api/v1/tools/video-merger`) → Celery task `video_merge`.
- Audio extractor (`/api/v1/tools/audio-extractor`) → Celery task `audio_extract`.
- Subtitle generator (`/api/v1/tools/subtitle-generator`) → Celery task `subtitle_generate`.
- Thumbnail resizer (`/api/v1/tools/thumbnail-resizer`) → Celery task `thumbnail_resize` + Pillow.

Semua request dicatat ke `usage_history` untuk audit ringan.

## 10. Konfigurasi Docker
```bash
docker compose up --build
```
Service:
- `web` (FastAPI)
- `worker` (Celery)
- `db` (PostgreSQL)
- `redis`
- `nginx`

## 11. Quick Start
```bash
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload
```

## 12. Roadmap MVP → Full Version
### MVP (sekarang)
- Auth, dashboard, 50 catalog tools, 5 real media tools, queue background job, logging dasar.

### v1.0
- Implementasi seluruh 50 tools, favorite toggle, real notification center, full settings.

### v1.5
- Team workspace, per-project access, granular RBAC matrix, audit explorer, report export.

### v2.0
- Plugin architecture, API marketplace, usage billing, SSO enterprise.

---

## Keamanan & Legal Compliance
- Hanya fitur legal dan aman.
- Tool jaringan harus dibatasi untuk aset milik sendiri (`OWNED_ASSET_WHITELIST`).
- Gunakan validasi input, rate limiting, logging, dan error handling.
- Tidak ada fitur phishing, cracking, exploit automation, credential theft, spam attack, atau tracking ilegal.
