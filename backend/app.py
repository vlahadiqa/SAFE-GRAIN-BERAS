"""
Safe Grain v3 — Backend
FastAPI + SQLAlchemy (SQLite) + YOLOv8
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Session
from ultralytics import YOLO
import cv2
import numpy as np
import base64
import os
import time
import logging
from datetime import datetime

# ─────────────────────────────────────────
#  Logging
# ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("safe-grain")

# ─────────────────────────────────────────
#  App & CORS
# ─────────────────────────────────────────
app = FastAPI(
    title="Safe Grain API v3",
    description="Smart Rice Detector — YOLOv8 + FastAPI + SQLite",
    version="3.0.0",
)

import os as _os

ALLOWED_ORIGINS = _os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,https://safe-grain-beras.vercel.app").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
#  Database (SQLite via SQLAlchemy)
# ─────────────────────────────────────────
BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "safegrain.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class ScanHistory(Base):
    __tablename__ = "scan_history"

    id                = Column(Integer, primary_key=True, index=True)
    timestamp         = Column(DateTime, default=datetime.utcnow)
    utuh              = Column(Integer, default=0)
    pecah             = Column(Integer, default=0)
    benda_asing       = Column(Integer, default=0)
    grade             = Column(String)
    label             = Column(String)
    percent_utuh      = Column(Float, default=0.0)
    estimated_price   = Column(Float, default=0.0)
    processing_time_ms= Column(Float, default=0.0)


Base.metadata.create_all(bind=engine)
logger.info("✅ Database siap: %s", DB_PATH)

# ─────────────────────────────────────────
#  Load YOLOv8 model
# ─────────────────────────────────────────
MODEL_PATH = os.path.join(BASE_DIR, "best.pt")

logger.info("⏳ Memuat model YOLOv8...")
try:
    model = YOLO(MODEL_PATH)
    logger.info("✅ Model berhasil dimuat!")
except Exception as exc:
    logger.error("❌ Gagal memuat model: %s", exc)
    raise RuntimeError(f"Gagal memuat model: {exc}")

# ─────────────────────────────────────────
#  Konstanta deteksi
# ─────────────────────────────────────────
GLOBAL_CONF       = 0.60
IOU_THRESHOLD     = 0.65
MIN_AREA_BERAS    = 150
MIN_AREA_BATU     = 250
CONF_BATU_MIN     = 0.60

COLOR_ASING  = (0, 0, 255)    # Merah
COLOR_UTUH   = (0, 255, 0)    # Hijau
COLOR_PECAH  = (0, 255, 255)  # Kuning

# ─────────────────────────────────────────
#  Grading logic (mirrors frontend)
# ─────────────────────────────────────────
def calculate_grade(utuh: int, pecah: int, benda_asing: int, base_price: float = 0):
    # Hitung persentase butir utuh dari SEMUA objek terdeteksi (termasuk benda asing)
    total = utuh + pecah + benda_asing
    pct   = (utuh / total * 100) if total > 0 else 0.0

    if pct >= 85:
        grade, label, final = "PREMIUM", "LOLOS QC — GRADE A", base_price
    else:
        grade, label, final = "MEDIUM", "LOLOS QC — GRADE B", base_price * 0.9

    if benda_asing > 2:
        grade, label, final = "TIDAK BERSIH", "TIDAK LAYAK KONSUMSI", 0
    elif benda_asing > 0:
        grade, label, final = "LOW", "REJECT — PERLU SORTIR ULANG", final * 0.8

    return grade, label, round(pct, 1), round(final)


# ─────────────────────────────────────────
#  Schemas
# ─────────────────────────────────────────
class DetectRequest(BaseModel):
    image: str
    base_price: float = Field(default=0.0, ge=0.0, description="Harga dasar beras per kg (tidak boleh negatif)")

    @field_validator("image")
    @classmethod
    def not_empty(cls, v):
        if not v or len(v) < 50:
            raise ValueError("Field 'image' kosong atau terlalu pendek.")
        return v


class DetectResponse(BaseModel):
    status: str
    utuh: int
    pecah: int
    benda_asing: int
    debug_image: str
    timestamp: str
    processing_time_ms: float


# ─────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────
def decode_image(b64: str) -> np.ndarray:
    parts = b64.split(",")
    raw   = parts[1] if len(parts) > 1 else parts[0]
    arr   = np.frombuffer(base64.b64decode(raw), np.uint8)
    img   = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Gambar tidak valid. Pastikan format JPEG/PNG.")
    return img


def encode_image(img: np.ndarray) -> str:
    _, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return "data:image/jpeg;base64," + base64.b64encode(buf).decode()


def run_detection(img: np.ndarray):
    results   = model(img, conf=GLOBAL_CONF, iou=IOU_THRESHOLD)
    counts    = {"utuh": 0, "pecah": 0, "benda_asing": 0}
    debug_img = img.copy()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf   = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0]
            area   = (x2 - x1) * (y2 - y1)
            valid  = False
            color  = (255, 255, 255)

            if cls_id == 0 and area > MIN_AREA_BATU and conf > CONF_BATU_MIN:
                counts["benda_asing"] += 1; valid = True; color = COLOR_ASING
            elif cls_id == 1 and area > MIN_AREA_BERAS:
                counts["utuh"] += 1;        valid = True; color = COLOR_UTUH
            elif cls_id == 2 and area > MIN_AREA_BERAS:
                counts["pecah"] += 1;       valid = True; color = COLOR_PECAH

            if valid:
                cv2.rectangle(debug_img, tuple(map(int, [x1, y1])), tuple(map(int, [x2, y2])), color, 2)

    return counts, debug_img


# ─────────────────────────────────────────
#  Endpoints
# ─────────────────────────────────────────
@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "ok", "version": "3.0.0", "timestamp": datetime.now().isoformat()}


@app.post("/detect", response_model=DetectResponse, tags=["Deteksi"])
async def detect_rice(payload: DetectRequest):
    t0 = time.perf_counter()

    try:
        img = decode_image(payload.image)
    except ValueError as e:
        raise HTTPException(400, str(e))

    try:
        counts, debug_img = run_detection(img)
    except Exception as e:
        logger.error("Deteksi error: %s", e)
        raise HTTPException(500, f"Deteksi gagal: {e}")

    ms = round((time.perf_counter() - t0) * 1000, 2)
    logger.info("📊 Utuh=%d Pecah=%d Asing=%d | %.0f ms",
                counts["utuh"], counts["pecah"], counts["benda_asing"], ms)

    # Save to DB
    grade, label, pct, est_price = calculate_grade(
        counts["utuh"], counts["pecah"], counts["benda_asing"], payload.base_price
    )
    with Session(engine) as db:
        db.add(ScanHistory(
            utuh=counts["utuh"],
            pecah=counts["pecah"],
            benda_asing=counts["benda_asing"],
            grade=grade,
            label=label,
            percent_utuh=pct,
            estimated_price=est_price,
            processing_time_ms=ms,
        ))
        db.commit()

    return DetectResponse(
        status="success",
        utuh=counts["utuh"],
        pecah=counts["pecah"],
        benda_asing=counts["benda_asing"],
        debug_image=encode_image(debug_img),
        timestamp=datetime.now().isoformat(),
        processing_time_ms=ms,
    )


@app.get("/history", tags=["Riwayat"])
async def get_history(limit: int = 20):
    with Session(engine) as db:
        rows = (
            db.query(ScanHistory)
            .order_by(ScanHistory.id.desc())
            .limit(limit)
            .all()
        )
    return {
        "items": [
            {
                "id":               r.id,
                "timestamp":        r.timestamp.isoformat() if r.timestamp else None,
                "utuh":             r.utuh,
                "pecah":            r.pecah,
                "benda_asing":      r.benda_asing,
                "grade":            r.grade,
                "label":            r.label,
                "percent_utuh":     r.percent_utuh,
                "estimated_price":  r.estimated_price,
                "processing_time_ms": r.processing_time_ms,
            }
            for r in rows
        ]
    }


@app.delete("/history", tags=["Riwayat"])
async def delete_history():
    with Session(engine) as db:
        deleted = db.query(ScanHistory).delete()
        db.commit()
    return {"deleted": deleted}


@app.get("/stats", tags=["Monitoring"])
async def get_stats():
    with Session(engine) as db:
        total = db.query(func.count(ScanHistory.id)).scalar() or 0
        avg_pct = db.query(func.avg(ScanHistory.percent_utuh)).scalar()
        grade_counts = (
            db.query(ScanHistory.grade, func.count(ScanHistory.id))
            .group_by(ScanHistory.grade)
            .all()
        )
    return {
        "total_scans":       total,
        "avg_percent_utuh":  round(avg_pct or 0, 1),
        "grade_distribution": {g: c for g, c in grade_counts},
    }


# ─────────────────────────────────────────
#  Static files (serve built React app)
# ─────────────────────────────────────────
DIST = os.path.join(BASE_DIR, "..", "frontend", "dist")
if os.path.isdir(DIST):
    @app.get("/", include_in_schema=False)
    async def root():
        return FileResponse(os.path.join(DIST, "index.html"))

    app.mount("/", StaticFiles(directory=DIST, html=True), name="static")


# ─────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Safe Grain API v3.0")
    logger.info("   Docs  : http://127.0.0.1:5000/docs")
    logger.info("   Health: http://127.0.0.1:5000/health")
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=False)
