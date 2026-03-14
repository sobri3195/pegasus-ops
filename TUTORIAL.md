# Tutorial Pegasus Ops (Step-by-Step)

Dokumen ini berisi alur praktis untuk menjalankan Pegasus Ops dari nol sampai mencoba 5 fitur media utama.

## 1) Prasyarat
- Python 3.11+
- PostgreSQL aktif
- Redis aktif
- FFmpeg terpasang (untuk job media)
- (Opsional) Docker & Docker Compose

## 2) Setup lokal cepat
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload
```

Aplikasi akan aktif di `http://127.0.0.1:8000`.

## 3) Menjalankan worker Celery
Buka terminal baru:
```bash
source .venv/bin/activate
celery -A app.tasks.celery_app.celery worker --loglevel=info
```

## 4) Coba alur autentikasi
1. Buka `/login`.
2. Daftar akun baru dari form register.
3. Setelah sukses, Anda akan diarahkan ke `/dashboard`.

## 5) Coba 5 fitur media via API
Semua endpoint ada di prefix `/api/v1/tools`.

### A. Video cutter
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/video-cutter \
  -F 'input_file=@sample.mp4' \
  -F 'start=00:00:02' \
  -F 'duration=00:00:05' \
  -b 'access_token=<cookie-token>'
```

### B. Video merger
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/video-merger \
  -F 'file_list_path=/tmp/files.txt' \
  -b 'access_token=<cookie-token>'
```

### C. Audio extractor
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/audio-extractor \
  -F 'input_file=@sample.mp4' \
  -b 'access_token=<cookie-token>'
```

### D. Subtitle generator
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/subtitle-generator \
  -F 'input_file=@sample.mp4' \
  -b 'access_token=<cookie-token>'
```

### E. Thumbnail resizer
```bash
curl -X POST http://127.0.0.1:8000/api/v1/tools/thumbnail-resizer \
  -F 'input_file=@sample.jpg' \
  -F 'width=1280' \
  -F 'height=720' \
  -b 'access_token=<cookie-token>'
```

## 6) Menambah modul/fitur baru
1. Tambahkan business logic pada `app/services/`.
2. Hubungkan endpoint pada `app/api/v1/`.
3. Jika async/heavy, buat task di `app/tasks/`.
4. Tambahkan model+schema bila butuh persistensi.
5. Tambahkan test di `tests/`.

## 7) Jalankan pengujian
```bash
pytest -q
```

## 8) Troubleshooting singkat
- **Login redirect loop**: pastikan cookie `access_token` terset.
- **Job tidak berjalan**: cek worker Celery aktif dan Redis hidup.
- **FFmpeg error**: pastikan ffmpeg ada di PATH sistem.
- **DB error**: jalankan ulang `alembic upgrade head`.
