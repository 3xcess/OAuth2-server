from fastapi import APIRouter
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import json
import base64
from ..sec.jwt import PUBLIC_KEY

router = APIRouter(tags=["well-known"])

def b64url_uint(n: int) -> str:
    """Base64URL-encode an integer per RFC 7517."""
    b = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode("ascii")

@router.get("/.well-known/jwks.json")
def get_jwks():
    """
    Publish the public key in JWK (JSON Web Key) format
    so external clients can verify JWTs.
    """
    public_key = serialization.load_pem_public_key(PUBLIC_KEY.encode())
    numbers: rsa.RSAPublicNumbers = public_key.public_numbers()

    jwk = {
        "kty": "RSA",
        "alg": "RS256",
        "use": "sig",
        "kid": "main-key-1",
        "n": b64url_uint(numbers.n),
        "e": b64url_uint(numbers.e),
    }

    return {"keys": [jwk]}