from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
import base64, hashlib

from ..db import SessionLocal
from ..models import AuthCode, OAuthClient
from ..sec.jwt import create_access_token

router = APIRouter(prefix="/oauth", tags=["token"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_pkce(code_verifier: str, code_challenge: str, method: str = "S256"):
    if not code_challenge:
        return True
    if method == "S256":
        new_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode()).digest()
        ).rstrip(b"=").decode()
        return new_challenge == code_challenge
    return False

@router.post("/token")
def token(
    grant_type: str = Form(...),
    code: str = Form(...),
    redirect_uri: str = Form(...),
    client_id: str = Form(...),
    code_verifier: str = Form(None),
    db: Session = Depends(get_db),
):
    if grant_type != "authorization_code":
        raise HTTPException(status_code=400, detail="Unsupported grant_type")


    auth_code = db.query(AuthCode).filter(AuthCode.code == code).first()
    if not auth_code:
        raise HTTPException(status_code=400, detail="Invalid authorization code")
    if datetime.utcnow() > auth_code.expires_at:
        raise HTTPException(status_code=400, detail="Authorization code expired")
    if auth_code.client_id != client_id:
        raise HTTPException(status_code=400, detail="Client mismatch")
    if auth_code.redirect_uri != redirect_uri:
        raise HTTPException(status_code=400, detail="Redirect URI mismatch")


    if not verify_pkce(code_verifier, auth_code.code_challenge, auth_code.code_challenge_method):
        raise HTTPException(status_code=400, detail="PKCE verification failed")


    access_token = create_access_token(
        sub=str(auth_code.user_id),
        client_id=client_id,
        scope=auth_code.scope,
    )


    db.delete(auth_code)
    db.commit()


    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 900,
        "scope": auth_code.scope
    }
