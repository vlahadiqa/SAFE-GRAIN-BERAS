<div align="center">

# 🌾 Safe Grain v3.0

### Smart Rice Detector — AI-Powered Rice Quality Analysis

**YOLOv8 · FastAPI · React · Vite · SQLite**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=flat-square&logo=vite&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-FF6B35?style=flat-square)

</div>

---

## 📖 Overview

**Safe Grain** adalah sistem deteksi kualitas beras berbasis AI Computer Vision yang dikembangkan
sebagai Tugas Besar Mata Kuliah Kecerdasan Buatan. Sistem ini mengklasifikasi butir beras secara
otomatis menggunakan model **YOLOv8** yang dilatih pada dataset beras lokal.

### Kemampuan Deteksi

| Kelas | Deskripsi | Warna BBox |
|---|---|---|
| 🟢 Butir Utuh | Beras tidak patah, kualitas terbaik | Hijau |
| 🟡 Butir Pecah | Beras patah sebagian | Kuning |
| 🔴 Benda Asing | Batu, kotoran, atau objek non-beras | Merah |

### Sistem Grading

| Grade | Kondisi | Harga |
|---|---|---|
| **PREMIUM (A)** | ≥85% butir utuh, 0 benda asing | 100% |
| **MEDIUM (B)** | <85% butir utuh, 0 benda asing | 90% |
| **LOW** | 1–2 benda asing terdeteksi | 72% |
| **TIDAK BERSIH** | >2 benda asing | Rp 0 |

---

## 🏗️ Arsitektur Sistem

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
│               FastAPI Backend (Python)               │
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

## 📁 Struktur Proyek

```
safegrain-v3/
├── backend/
│   ├── app.py              ← FastAPI + SQLAlchemy + YOLO inference
│   ├── best.pt             ← Model YOLOv8 terlatih (6MB)
│   ├── requirements.txt    ← Python dependencies
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
│   │   │   ├── api.js            ← Fetch wrapper
│   │   │   ├── grading.js        ← Grade calculation
│   │   │   └── pdfExport.js      ← jsPDF report
│   │   ├── pages/
│   │   │   ├── AboutPage.jsx     ← Tim & teknologi
│   │   │   └── StatsPage.jsx     ← Statistik & charts
│   │   ├── App.jsx               ← Root + routing + health check
│   │   └── index.css             ← Global styles + Tailwind
│   ├── index.html                ← SEO meta + favicon
│   └── vite.config.js            ← Vite + Tailwind + proxy
│
└── README.md
```

---

## 🚀 Cara Menjalankan

### Prasyarat
- Python 3.10+
- Node.js 18+
- File `best.pt` di folder `backend/`

### 1. Backend

```bash
cd safegrain-v3/backend

# Install dependencies
pip install -r requirements.txt

# Jalankan server
python app.py
```

Server berjalan di → `http://127.0.0.1:5000`

| URL | Keterangan |
|---|---|
| `http://127.0.0.1:5000/docs` | Swagger UI — dokumentasi API interaktif |
| `http://127.0.0.1:5000/health` | Status server |

### 2. Frontend (Development)

```bash
cd safegrain-v3/frontend

npm install
npm run dev
```

Buka browser → `http://localhost:5173`

### 3. Build Production

```bash
cd frontend && npm run build
# Kemudian akses via backend: http://127.0.0.1:5000
```

---

## 📡 API Reference

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

## ✨ Fitur Utama

- **🎯 Deteksi AI Real-time** — YOLOv8 dengan bounding box berwarna per kelas
- **📷 Live Camera Capture** — Foto langsung dari kamera device
- **🖱️ Drag & Drop Upload** — Upload gambar dengan seret atau klik
- **📊 Donut Chart** — Visualisasi proporsi butir utuh/pecah/asing
- **📈 Halaman Statistik** — Tren keutuhan, distribusi grade, bar chart
- **💾 Persistent History** — Riwayat scan tersimpan di SQLite
- **📄 Export PDF** — Laporan lengkap dengan jsPDF
- **🔔 Server Health Monitor** — Banner otomatis jika backend offline
- **🎨 Custom Design System** — Tailwind + token warna konsisten

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|---|---|
| AI/CV Model | YOLOv8 (Ultralytics) |
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| Frontend | React 18, Vite, Tailwind CSS |
| Charts | Recharts |
| PDF | jsPDF |
| Icons | Phosphor Icons |
| Upload | React Dropzone |

---

## 👥 Tim Pengembang

**Tugas Besar Mata Kuliah Kecerdasan Buatan**

| Divisi | Anggota |
|---|---|
| Computer Vision | Andy Bagus Oesmadi · Maulidah Imroatus Solehah · Mishal Eman |
| Front-End, Back-End & UI/UX | Venerdi Dinarsa Narendra Putra C. · Vlahadiqa Runayasha Khandeva W. · Zacky Maulanaa |
| System Analyst | Muhammad Zidan Al Farezel · Vichars Mazcheranou Hafizh |

---

<div align="center">
  <sub>Safe Grain v3.0 · Smart Rice Detector · Built with ❤️ using YOLOv8 + FastAPI + React</sub>
</div>
