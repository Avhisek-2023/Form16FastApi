from fastapi import FastAPI, UploadFile, File
import os
from .extractor.parse_cpy import extract_form16_data
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://taxyaar.com"
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


app.include_router(upload_router.router,prefix="/api")