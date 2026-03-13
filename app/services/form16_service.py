import os
from fastapi import UploadFile
from app.extractor.parse_cpy import extract_form16_data

UPLOAD_FOLDER = "app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


async def process_form16(pdf: UploadFile):

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