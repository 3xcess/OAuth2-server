from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from ..db import SessionLocal
from ..models import OAuthClient, AuthCode, User

router = APIRouter(prefix="/oauth", tags=["authorization"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/authorize")
def authorize(
    response_type: str = Query(..., regex="^code$"),
    client_id: str = Query(...),
    redirect_uri: str = Query(...),
    scope: str = Query("user.read"),
    state: str = Query(None),
    code_challenge: str = Query(None),
    code_challenge_method: str = Query("S256"),
    username: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db),
):
    
    client = db.query(OAuthClient).filter_by(client_id=client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Invalid client_id")

    allowed_uris = [u.strip() for u in client.redirect_uris.split(",")]
    if redirect_uri not in allowed_uris:
        raise HTTPException(status_code=400, detail="Invalid redirect URI")

    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid user")

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    auth_code = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=5)

    new_code = AuthCode(
        code=auth_code,
        user_id=user.id,
        client_id=client_id,
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        scope=scope,
        expires_at=expires,
    )
    db.add(new_code)
    db.commit()

    from fastapi.responses import RedirectResponse
    redirect_url = f"{redirect_uri}?code={auth_code}"
    if state:
        redirect_url += f"&state={state}"

    return RedirectResponse(url=redirect_url)
