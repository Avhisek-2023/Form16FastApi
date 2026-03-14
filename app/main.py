from fastapi import FastAPI, UploadFile, File
import os
from .extractor.parse_cpy import extract_form16_data
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/upload")
async def upload_file(pdf: UploadFile = File(...)):
    
    filepath = os.path.join(UPLOAD_FOLDER, pdf.filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await pdf.read())

    try:
        data = extract_form16_data(filepath)
        return {
            "status": "success",
            "data": data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }