<div align="center">

# Safe Grain — Frontend

### React 19 · Vite 8 · Tailwind CSS 4

![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=flat-square&logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-4-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)
![Vercel](https://img.shields.io/badge/Deploy-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)

**Live Demo:** https://safe-grain-beras.vercel.app

</div>

---

## Tentang

Antarmuka web untuk sistem deteksi kualitas beras **Safe Grain**. Pengguna dapat mengunggah foto beras atau menggunakan kamera device secara langsung, lalu menerima hasil analisis kualitas berbasis AI dalam hitungan detik.

---

## Fitur

- **Upload Gambar** — Drag & drop atau klik untuk memilih file
- **Live Camera** — Ambil foto langsung dari kamera device
- **Hasil Deteksi Real-time** — Bounding box berwarna per kelas (utuh/pecah/asing)
- **Donut Chart** — Visualisasi proporsi butir dengan Recharts
- **Sistem Grading** — Grade PREMIUM / MEDIUM / LOW / TIDAK BERSIH otomatis
- **Estimasi Harga** — Kalkulasi harga berdasarkan grade
- **Halaman Statistik** — Tren keutuhan, distribusi grade, riwayat scan
- **Export PDF** — Laporan lengkap dengan jsPDF
- **Health Monitor** — Banner otomatis jika backend offline

---

## Struktur Folder

```
src/
├── components/
│   ├── Sidebar.jsx         ← Navigasi + logo
│   ├── UploadPanel.jsx     ← Upload + kamera + tombol scan
│   ├── ResultPanel.jsx     ← Grade + chart + export PDF
│   ├── StatCard.jsx        ← Animated counter card
│   ├── GradeChart.jsx      ← Donut chart (Recharts)
│   ├── HistoryTable.jsx    ← Tabel riwayat scan
│   └── ErrorView.jsx       ← Tampilan error states
├── hooks/
│   ├── useDetection.js     ← Logika scan & state management
│   └── useHistory.js       ← Fetch & kelola riwayat
├── utils/
│   ├── api.js              ← Fetch wrapper + base URL
│   ├── grading.js          ← Kalkulasi grade & harga
│   └── pdfExport.js        ← Generate laporan jsPDF
├── pages/
│   ├── StatsPage.jsx       ← Statistik & area chart
│   └── AboutPage.jsx       ← Info tim & teknologi
├── App.jsx                 ← Root component + routing + health check
└── index.css               ← Global styles + Tailwind tokens
```

---

## Tech Stack

| Paket | Versi | Kegunaan |
|---|---|---|
| React | 19 | UI framework |
| Vite | 8 | Build tool + dev server |
| Tailwind CSS | 4 | Utility-first styling |
| Recharts | 3 | Chart (donut, area, bar) |
| jsPDF | 4 | Export laporan PDF |
| Phosphor Icons | 2 | Icon library |
| React Dropzone | 15 | Drag & drop upload |
| Framer Motion | 12 | Animasi UI |

---

## Menjalankan Lokal

### Prasyarat

- Node.js 18+
- Backend Safe Grain berjalan di `http://localhost:5000`

### Instalasi & Jalankan

```bash
# Install dependensi
npm install

# Jalankan dev server
npm run dev
```

Buka browser → `http://localhost:5173`

Dev proxy di `vite.config.js` akan meneruskan request `/detect`, `/history`, `/stats`, `/health` ke backend lokal secara otomatis — tidak perlu konfigurasi CORS tambahan.

### Build Production

```bash
npm run build
```

Output di folder `dist/`. Siap di-serve oleh backend FastAPI atau di-deploy ke Vercel.

### Perintah Lainnya

```bash
npm run lint      # Cek ESLint
npm run preview   # Preview hasil build production
```

---

## Environment Variable

Secara default, `src/utils/api.js` menggunakan URL backend dari environment variable saat build:

| Variable | Default | Keterangan |
|---|---|---|
| `VITE_API_URL` | `""` (kosong) | URL backend production. Kosongkan untuk dev proxy lokal |

Untuk production, set di Vercel dashboard:
```
VITE_API_URL=https://safe-grain-beras-production.up.railway.app
```

---

## Deploy ke Vercel

1. Push kode ke GitHub
2. Import repository di [vercel.com](https://vercel.com)
3. Set **Root Directory** ke `frontend`
4. Tambahkan environment variable `VITE_API_URL`
5. Deploy

---

## Tim

**Tugas Besar Mata Kuliah Kecerdasan Buatan**

| Divisi | Anggota |
|---|---|
| Front-End & UI/UX | Venerdi Dinarsa Narendra Putra C · Vlahadiqa Runayasha Khandeva W |
| Computer Vision | Andy Bagus Oesmadi · Zacky Maulana |

---

<div align="center">
  <sub>Safe Grain v3.0 · Frontend · React + Vite + Tailwind</sub>
</div>
