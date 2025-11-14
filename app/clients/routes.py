from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import secrets
from ..db import SessionLocal
from ..models import OAuthClient

router = APIRouter(prefix="/clients", tags=["clients"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register_client")
def register_client(redirect_uris: str, is_confidential: bool = True, db: Session = Depends(get_db)):
    client_id = secrets.token_urlsafe(16)
    client_secret = secrets.token_urlsafe(32) if is_confidential else None

    new_client = OAuthClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uris=redirect_uris,
        is_confidential=is_confidential
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return {
        "client_id": new_client.client_id,
        "client_secret": new_client.client_secret,
        "redirect_uris": new_client.redirect_uris,
        "is_confidential": new_client.is_confidential
    }