from fastapi import APIRouter, Header, HTTPException, Depends
from jose import jwt, JWTError
from ..sec.jwt import PUBLIC_KEY, ALGORITHM
from ..db import SessionLocal
from ..models import User
from ..auth.revoke import is_token_revoked

router = APIRouter(prefix="/api", tags=["resource"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_token(authorization: str = Header(None, convert_underscores=False)):
    """Extract and verify Bearer token."""
    allowed_audiences = ["LnOBKY9x8T_37PXhii0-Kw"]
    if not authorization or not authorization.startswith("Bearer "):
        print(authorization)
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], options={"verify_aud": False})
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    if payload.get("aud") not in allowed_audiences:
        raise HTTPException(status_code=401, detail="Invalid audience")
    
    if is_token_revoked(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    return payload

@router.get("/profile")
def get_profile(payload: dict = Depends(verify_token), db=Depends(get_db)):
    """Return basic user info if token valid."""
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")


    if "user.read" not in payload.get("scope", ""):
        raise HTTPException(status_code=403, detail="Insufficient scope")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.id,
        "username": user.username,
        "scopes": payload.get("scope"),
        "issued_to_client": payload.get("aud"),
        "expires_at": payload.get("exp"),
    }