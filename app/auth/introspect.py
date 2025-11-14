from fastapi import APIRouter, Form, HTTPException
from jose import jwt, JWTError
from ..sec.jwt import PUBLIC_KEY, ALGORITHM

router = APIRouter(prefix="/oauth", tags=["introspection"])

# RFC 7662
@router.post("/introspect")
def introspect(token: str = Form(...)):
    """
    Verify a token and return its claims if valid.
    """
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        return {
            "active": True,
            "iss": payload.get("iss"),
            "sub": payload.get("sub"),
            "aud": payload.get("aud"),
            "scope": payload.get("scope"),
            "exp": payload.get("exp"),
            "iat": payload.get("iat"),
        }
    
    except JWTError:
        return {"active": False}