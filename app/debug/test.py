from fastapi import APIRouter, Header, HTTPException
from jose import jwt, JWTError
from ..sec.jwt import PUBLIC_KEY, ALGORITHM

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/token_info")
def token_info(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=400, detail="Missing Authorization header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header format")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},  # for convenience
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {e}")

    return {"decoded_payload": payload}
