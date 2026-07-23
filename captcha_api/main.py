from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from app.detector import detect_gap
from app.repositories.detection_repository import DetectionRepository

app = FastAPI(
    title="Captcha Gap Detection API",
    version="1.0.0",
    description="API untuk mendeteksi posisi gap slider captcha menggunakan YOLO."
)


@app.get("/")
def root():
    return {
        "status": "API aktif",
        "message": "Kirim POST ke /detect dengan file gambar"
    }


@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    result = await detect_gap(file)
    DetectionRepository.save(result)
    return JSONResponse(result)
