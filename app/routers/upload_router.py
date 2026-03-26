from fastapi import APIRouter, UploadFile, File, Depends
# from app.services.
from app.schemas.form16_schemas import Form16Response
from app.services.form16_service import process_form16
from app.dependencies.client_auth import get_client_payload 
from app.utils.jwt import create_client_token

router = APIRouter()

@router.post("/upload", response_model=Form16Response)
async def upload_file(pdf: UploadFile = File(...),payload = Depends(get_client_payload)):
    return await process_form16(pdf)


@router.post("/getClientToken")
def client_token():
    return create_client_token()     