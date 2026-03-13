from fastapi import APIRouter, UploadFile, File
# from app.services.
from app.schemas.form16_schemas import Form16Response

router = APIRouter()

@router.post("/upload", response_model=Form16Response)
async def upload_file(pdf: UploadFile = File(...)):
    return await process_form16(pdf)