<div align="center">

# Safe Grain v3.0

### Smart Rice Detector — AI-Powered Rice Quality Analysis

**YOLOv8 · FastAPI · React · Vite · SQLite**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=flat-square&logo=vite&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=flat-square)
![Railway](https://img.shields.io/badge/Backend-Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

</div>

---

## Tentang Proyek

**Safe Grain** adalah sistem deteksi kualitas beras berbasis AI Computer Vision yang dikembangkan sebagai Tugas Besar Mata Kuliah Kecerdasan Buatan. Sistem ini mengklasifikasi butir beras secara otomatis menggunakan model **YOLOv8** yang dilatih pada dataset beras lokal.

### Kemampuan Deteksi

| Kelas | Deskripsi | Warna BBox |
|---|---|---|
| Butir Utuh | Beras tidak patah, kualitas terbaik | Hijau |
| Butir Pecah | Beras patah sebagian | Kuning |
| Benda Asing | Batu, kotoran, atau objek non-beras | Merah |

### Sistem Grading

| Grade | Kondisi | Harga |
|---|---|---|
| **PREMIUM (A)** | ≥85% butir utuh, 0 benda asing | 100% |
| **MEDIUM (B)** | <85% butir utuh, 0 benda asing | 90% |
| **LOW** | 1–2 benda asing terdeteksi | 72% |
| **TIDAK BERSIH** | >2 benda asing | Rp 0 |

---

## Deployment

| Layer | Platform | URL |
|---|---|---|
| Backend (FastAPI) | Railway | https://safe-grain-beras-production.up.railway.app |
| Frontend (React) | Vercel | https://safe-grain-beras.vercel.app |

### Catatan Deployment

Backend di-deploy menggunakan Docker di Railway. Image menggunakan `python:3.11-slim` dengan dependensi sistem untuk OpenCV (`libgl1`, `libglib2.0-0`, dll.) dan menjalankan server via `uvicorn` pada port yang disediakan Railway secara otomatis lewat environment variable `$PORT`.

Endpoint publik backend:

| URL | Keterangan |
|---|---|
| `https://safe-grain-beras-production.up.railway.app/docs` | Swagger UI |
| `https://safe-grain-beras-production.up.railway.app/health` | Status server |

---

## Arsitektur Sistem

```
┌─────────────────────────────────────────────────────┐
│                    Browser (React)                   │
│  ┌──────────┐  ┌────────────┐  ┌─────────────────┐  │
│  │ Upload   │  │  Result    │  │   Statistik     │  │
│  │ Panel    │  │  Panel     │  │   Page          │  │
│  │+ Camera  │  │+ Donut     │  │+ Area Chart     │  │
│  │+ Dropzone│  │+ PDF Export│  │+ Grade Pie      │  │
│  └────┬─────┘  └─────┬──────┘  └────────────────-┘  │
│       │  HTTP POST /detect     HTTP GET /stats       │
└───────┼─────────────────────────────────────────────-┘
        │
┌───────▼──────────────────────────────────────────────┐
│          FastAPI Backend (Railway — Docker)          │
│  ┌─────────────────────┐  ┌────────────────────────┐ │
│  │   POST /detect      │  │  GET  /history         │ │
│  │   GET  /health      │  │  DELETE /history       │ │
│  │   GET  /stats       │  │  StaticFiles (dist/)   │ │
│  └──────────┬──────────┘  └────────────────────────┘ │
│             │                                         │
│  ┌──────────▼──────────┐  ┌────────────────────────┐ │
│  │  YOLOv8 (best.pt)   │  │  SQLite (safegrain.db) │ │
│  │  Inference Engine   │  │  ScanHistory Table     │ │
│  └─────────────────────┘  └────────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

---

## Struktur Proyek

```
SAFE-GRAIN-BERAS/
├── backend/
│   ├── app.py              ← FastAPI + SQLAlchemy + YOLO inference
│   ├── best.pt             ← Model YOLOv8 terlatih (6MB)
│   ├── requirements.txt    ← Python dependencies
│   ├── Dockerfile          ← Docker config untuk Railway
│   ├── Procfile            ← Procfile fallback
│   └── safegrain.db        ← SQLite DB (auto-generated)
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.jsx       ← Navigasi + logo
│   │   │   ├── UploadPanel.jsx   ← Upload + Live Camera + Scan
│   │   │   ├── ResultPanel.jsx   ← Grade + Chart + PDF
│   │   │   ├── StatCard.jsx      ← Animated counter card
│   │   │   ├── GradeChart.jsx    ← Donut chart (Recharts)
│   │   │   ├── ErrorView.jsx     ← Error states
│   │   │   └── HistoryTable.jsx  ← Riwayat scan
│   │   ├── hooks/
│   │   │   ├── useDetection.js   ← Logika scan & state
│   │   │   └── useHistory.js     ← Fetch & manage history
│   │   ├── utils/
│   │   │   ├── api.js            ← Fetch wrapper + base URL
│   │   │   ├── grading.js        ← Grade calculation
│   │   │   └── pdfExport.js      ← jsPDF report
│   │   ├── pages/
│   │   │   ├── AboutPage.jsx     ← Tim & teknologi
│   │   │   └── StatsPage.jsx     ← Statistik & charts
│   │   ├── App.jsx               ← Root + routing + health check
│   │   └── index.css             ← Global styles + Tailwind
│   ├── index.html                ← SEO meta + favicon
│   └── vite.config.js            ← Vite + Tailwind + dev proxy
│
└── README.md
```

---

## Cara Menjalankan (Lokal)

### Prasyarat

- Python 3.10+
- Node.js 18+
- File `best.pt` di folder `backend/`

### 1. Backend

```bash
cd backend

pip install -r requirements.txt

python app.py
```

Server berjalan di `http://127.0.0.1:5000`

| URL | Keterangan |
|---|---|
| `http://127.0.0.1:5000/docs` | Swagger UI |
| `http://127.0.0.1:5000/health` | Status server |

### 2. Frontend (Development)

```bash
cd frontend

npm install
npm run dev
```

Buka browser → `http://localhost:5173`

Dev proxy sudah dikonfigurasi di `vite.config.js` sehingga request ke `/detect`, `/history`, `/stats`, `/health` diteruskan otomatis ke backend lokal.

### 3. Build Production

```bash
cd frontend && npm run build
```

Output di `frontend/dist/`. Backend FastAPI sudah dikonfigurasi untuk serve folder `dist/` sebagai static files.

---

## Deploy ke Railway (Backend)

### Prasyarat

- Akun Railway
- Railway CLI atau push via GitHub

### Langkah

```bash
# Login Railway CLI
railway login

# Masuk ke folder backend
cd backend

# Link ke project Railway (atau buat baru)
railway init

# Deploy
railway up
```

Railway akan otomatis mendeteksi `Dockerfile` dan menggunakannya untuk build. Environment variable `PORT` disediakan Railway secara otomatis.

Pastikan `best.pt` ikut ter-push ke Railway. File ini tidak boleh ada di `.gitignore` karena dibutuhkan saat runtime.

---

## API Reference

### `POST /detect`

Deteksi kualitas beras dari gambar.

**Request:**
```json
{ "image": "data:image/jpeg;base64,..." }
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

### `GET /history?limit=20`

Riwayat scan terakhir dari database.

### `DELETE /history`

Hapus semua riwayat.

### `GET /stats`

Statistik agregat seluruh scan.

```json
{
  "total_scans": 47,
  "avg_percent_utuh": 72.4,
  "grade_distribution": { "PREMIUM": 18, "MEDIUM": 22, "LOW": 7 }
}
```

### `GET /health`

Status server dan versi.

---

## Fitur Utama

- **Deteksi AI Real-time** — YOLOv8 dengan bounding box berwarna per kelas
- **Live Camera Capture** — Foto langsung dari kamera device
- **Drag & Drop Upload** — Upload gambar dengan seret atau klik
- **Donut Chart** — Visualisasi proporsi butir utuh/pecah/asing
- **Halaman Statistik** — Tren keutuhan, distribusi grade, bar chart
- **Persistent History** — Riwayat scan tersimpan di SQLite
- **Export PDF** — Laporan lengkap dengan jsPDF
- **Server Health Monitor** — Banner otomatis jika backend offline
- **Custom Design System** — Tailwind + token warna konsisten

---

## Tech Stack

| Layer | Teknologi |
|---|---|
| AI/CV Model | YOLOv8 (Ultralytics) |
| Backend | Python 3.11, FastAPI, SQLAlchemy, SQLite |
| Frontend | React 19, Vite 8, Tailwind CSS 4 |
| Charts | Recharts |
| PDF | jsPDF |
| Icons | Phosphor Icons |
| Upload | React Dropzone |
| Containerization | Docker |
| Backend Hosting | Railway |

---

## Tim Pengembang

**Tugas Besar Mata Kuliah Kecerdasan Buatan**

| Divisi | Anggota |
|---|---|
| Computer Vision | Andy Bagus Oesmadi · Zacky Maulana |
| Front-End, Back-End & UI/UX | Venerdi Dinarsa Narendra Putra C · Vlahadiqa Runayasha Khandeva W |

---

<div align="center">
  <sub>Safe Grain v3.0 · Smart Rice Detector · Built with YOLOv8 + FastAPI + React</sub>
</div>
