<div align="center">

# Safe Grain — Backend

### FastAPI · YOLOv8 · SQLite · Docker

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=flat-square)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white)
![Railway](https://img.shields.io/badge/Deploy-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

**API:** https://safe-grain-beras-production.up.railway.app  
**Docs:** https://safe-grain-beras-production.up.railway.app/docs

</div>

---

## Tentang

Backend API untuk sistem deteksi kualitas beras **Safe Grain**. Menerima gambar beras dalam format Base64, menjalankan inferensi YOLOv8, menghitung grade kualitas, menyimpan riwayat ke SQLite, dan mengembalikan hasil beserta gambar anotasi.

---

## Endpoint API

| Method | Path | Keterangan |
|---|---|---|
| `POST` | `/detect` | Deteksi kualitas beras dari gambar |
| `GET` | `/history` | Riwayat scan terakhir |
| `DELETE` | `/history` | Hapus semua riwayat |
| `GET` | `/stats` | Statistik agregat seluruh scan |
| `GET` | `/health` | Status server & versi |
| `GET` | `/docs` | Swagger UI interaktif |

### `POST /detect`

**Request:**
```json
{
  "image": "data:image/jpeg;base64,...",
  "base_price": 15000
}
```

**Response:**
```json
{
  "status": "success",
  "utuh": 42,
  "pecah": 8,
  "benda_asing": 1,
  "debug_image": "data:image/jpeg;base64,...",
  "timestamp": "2025-06-09T10:30:00",
  "processing_time_ms": 312.5
}
```

### `GET /stats`

```json
{
  "total_scans": 47,
  "avg_percent_utuh": 72.4,
  "grade_distribution": { "PREMIUM": 18, "MEDIUM": 22, "LOW": 7 }
}
```

---

## Logika Deteksi

### Kelas YOLO

| Class ID | Label | Threshold Area | Warna BBox |
|---|---|---|---|
| 0 | Benda Asing (batu/kotoran) | 250px | Merah |
| 1 | Butir Utuh | 150px | Hijau |
| 2 | Butir Pecah | 150px | Kuning |

Confidence threshold global: **0.60** · IoU threshold: **0.65**

### Sistem Grading

| Grade | Kondisi | Harga |
|---|---|---|
| **PREMIUM** | ≥85% utuh, 0 benda asing | 100% |
| **MEDIUM** | <85% utuh, 0 benda asing | 90% |
| **LOW** | 1–2 benda asing | 72% |
| **TIDAK BERSIH** | >2 benda asing | Rp 0 |

---

## Menjalankan Lokal

### Prasyarat

- Python 3.10+
- File `best.pt` di folder `backend/`

### Instalasi & Jalankan

```bash
# Masuk ke folder backend
cd backend

# Install dependensi
pip install -r requirements.txt

# Jalankan server
python app.py
```

Server berjalan di `http://127.0.0.1:5000`

| URL | Keterangan |
|---|---|
| `http://127.0.0.1:5000/docs` | Swagger UI |
| `http://127.0.0.1:5000/health` | Status server |

### Menggunakan uvicorn langsung

```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

---

## Environment Variable

| Variable | Default | Keterangan |
|---|---|---|
| `ALLOWED_ORIGINS` | `http://localhost:5173,...` | Daftar origin yang diizinkan CORS (pisahkan dengan koma) |
| `PORT` | `8000` | Port server (disediakan otomatis oleh Railway) |

---

## Menjalankan dengan Docker

```bash
# Build image
docker build -t safe-grain-backend .

# Jalankan container
docker run -p 8000:8000 safe-grain-backend
```

---

## Deploy ke Railway

### Via GitHub (Rekomendasi)

1. Push kode ke GitHub (pastikan `best.pt` tidak ada di `.gitignore`)
2. Buat project baru di [railway.app](https://railway.app)
3. Pilih **Deploy from GitHub repo**
4. Set **Root Directory** ke `backend`
5. Railway akan otomatis mendeteksi `Dockerfile` dan melakukan build

### Via Railway CLI

```bash
# Login
railway login

# Masuk ke folder backend
cd backend

# Inisialisasi project (atau link ke yang sudah ada)
railway init

# Deploy
railway up
```

Environment variable `PORT` disediakan Railway secara otomatis. `ALLOWED_ORIGINS` perlu disetel dengan URL frontend production.

---

## Struktur Database

Tabel `scan_history` (SQLite — `safegrain.db`):

| Kolom | Tipe | Keterangan |
|---|---|---|
| `id` | INTEGER | Primary key |
| `timestamp` | DATETIME | Waktu scan |
| `utuh` | INTEGER | Jumlah butir utuh |
| `pecah` | INTEGER | Jumlah butir pecah |
| `benda_asing` | INTEGER | Jumlah benda asing |
| `grade` | STRING | PREMIUM / MEDIUM / LOW / TIDAK BERSIH |
| `label` | STRING | Label deskriptif hasil QC |
| `percent_utuh` | FLOAT | Persentase butir utuh |
| `estimated_price` | FLOAT | Estimasi harga per kg |
| `processing_time_ms` | FLOAT | Durasi inferensi (ms) |

---

## Dependencies

```
fastapi>=0.110.0
uvicorn[standard]>=0.29.0
python-multipart>=0.0.9
sqlalchemy>=2.0.0
ultralytics>=8.0.0
opencv-python-headless>=4.9.0
numpy>=1.24.0
Pillow>=10.0.0
```

---

## Tim

**Tugas Besar Mata Kuliah Kecerdasan Buatan**

| Divisi | Anggota |
|---|---|
| Computer Vision & Backend | Andy Bagus Oesmadi · Zacky Maulana |
| Front-End & UI/UX | Venerdi Dinarsa Narendra Putra C · Vlahadiqa Runayasha Khandeva W |

---

<div align="center">
  <sub>Safe Grain v3.0 · Backend · FastAPI + YOLOv8 + SQLite</sub>
</div>
