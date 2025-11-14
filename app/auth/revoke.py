from fastapi import APIRouter, Form
from typing import Set

router = APIRouter(prefix="/oauth", tags=["revocation"])
revoked_tokens: Set[str] = set()

@router.post("/revoke")
def revoke(token: str = Form(...)):
    """
    Mark a token as revoked.
    """
    revoked_tokens.add(token)
    return {"revoked": True}

def is_token_revoked(token: str) -> bool:
    return token in revoked_tokens
