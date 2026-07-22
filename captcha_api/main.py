from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import numpy as np
import cv2
import io

app = FastAPI(title="Captcha Gap Detection API")

# load model sekali aja saat server start (bukan tiap request, biar cepat)
model = YOLO("best.pt")

@app.get("/")
def root():
    return {"status": "API aktif", "message": "Kirim POST ke /detect dengan file gambar"}

@app.post("/detect")
async def detect_gap(file: UploadFile = File(...)):
    # validasi tipe file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File harus berupa gambar")

    # baca file upload jadi array gambar (tanpa simpan ke disk)
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise HTTPException(status_code=400, detail="Gagal membaca gambar, file mungkin corrupt")

    # inference
    results = model.predict(
        source=img,
        imgsz=640,
        conf=0.1,
        device="cpu",
        verbose=False
    )
    result = results[0]

    if len(result.boxes) == 0:
        return JSONResponse({
            "detected": False,
            "message": "Tidak ada gap terdeteksi"
        })

    # ambil box dengan confidence tertinggi
    best_idx = result.boxes.conf.argmax().item()
    box = result.boxes[best_idx]

    x1, y1, x2, y2 = box.xyxy[0].tolist()
    conf = box.conf[0].item()
    gap_center_x = (x1 + x2) / 2
    gap_center_y = (y1 + y2) / 2

    return JSONResponse({
        "detected": True,
        "confidence": round(conf, 4),
        "bbox": {
            "x1": round(x1, 2),
            "y1": round(y1, 2),
            "x2": round(x2, 2),
            "y2": round(y2, 2)
        },
        "gap_center": {
            "x": round(gap_center_x, 2),
            "y": round(gap_center_y, 2)
        }
    })