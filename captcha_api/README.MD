# Captcha Gap Detection API

API FastAPI untuk mendeteksi posisi gap slider captcha menggunakan YOLO dan menyimpan hasil deteksi ke database MySQL.

## Prasyarat

- Python 3.11 atau lebih baru
- MySQL Server
- File model YOLO `best.pt` berada di folder `captcha_api`
- `pip` sudah tersedia

## Instalasi

Masuk ke folder project API:

```powershell
cd C:\@user\slider-captcha\validate-captcha-slider-appium\captcha_api
```

Buat virtual environment:

```powershell
python -m venv .venv
```

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
pip install -r requirements.txt
```

## Konfigurasi Environment

Buat atau edit file `.env` di folder `captcha_api`:

```env
APP_NAME=Captcha Gap Detection API

MODEL_PATH=best.pt

YOLO_DEVICE=cpu
YOLO_IMAGE_SIZE=640
YOLO_CONFIDENCE=0.25

LOW_CONFIDENCE_THRESHOLD=0.5

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=captcha_ai
MYSQL_USER=root
MYSQL_PASSWORD=root
```

Sesuaikan `MYSQL_USER` dan `MYSQL_PASSWORD` dengan konfigurasi MySQL lokal.

## Setup Database

Buat database MySQL:

```sql
CREATE DATABASE captcha_ai;
```

Jalankan migrasi tabel:

```powershell
alembic upgrade head
```

Migrasi akan membuat tabel `detection_logs` untuk menyimpan hasil deteksi captcha.

## Menjalankan API

Jalankan server dari folder `captcha_api`:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API akan aktif di:

```text
http://127.0.0.1:8000
```

Dokumentasi Swagger tersedia di:

```text
http://127.0.0.1:8000/docs
```

## Test Deteksi

Test endpoint `/detect` menggunakan file `sample.png`:

```powershell
curl.exe -X POST "http://127.0.0.1:8000/detect" -F "file=@sample.png"
```

Jika berhasil, API akan mengembalikan hasil deteksi dan menyimpan data ke tabel `detection_logs`.

## Struktur Penting

```text
captcha_api/
  app/
    config.py
    database.py
    detector.py
    models.py
    repositories/
      detection_repository.py
  migrations/
  main.py
  requirements.txt
  alembic.ini
  best.pt
  .env
```

## Catatan

- Jika menggunakan GPU, ubah `YOLO_DEVICE` sesuai device yang tersedia.
- Jika model tidak ditemukan, pastikan `MODEL_PATH` mengarah ke file `best.pt`.
- Jika migrasi gagal, pastikan MySQL sudah berjalan dan database pada `MYSQL_DATABASE` sudah dibuat.
