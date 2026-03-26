from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from app.utils.jwt import verify_client_token

security = HTTPBearer()

def get_client_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    return verify_client_token(token)