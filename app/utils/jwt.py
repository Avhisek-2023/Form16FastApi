from jose import jwt
from datetime import datetime, timedelta
from app.config import settings

def create_client_token():
    payload = {
        "client": "TAXYAAR",
        "exp": datetime.utcnow() + timedelta(days=365)
    }  
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  
    return {"access_token" :token}


def verify_client_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        client = payload.get("client")

        if client != "TAXYAAR":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )