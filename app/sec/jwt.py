from datetime import datetime, timedelta
from jose import jwt

PRIVATE_KEY_PATH = "keys/private.pem"
PUBLIC_KEY_PATH  = "keys/public.pem"
ALGORITHM = "RS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()
with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()

def create_access_token(sub: str, client_id: str, scope: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "iss": "http://127.0.0.1:8000",
        "sub": sub,
        "aud": client_id,
        "scope": scope,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm=ALGORITHM)
    return token
