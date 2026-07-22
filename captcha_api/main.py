from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

from detector import detect_gap

app = FastAPI(
    title="Captcha Gap Detection API"
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
    return JSONResponse(result)