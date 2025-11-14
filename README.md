# 🛡️ OAuth2 Authorization Server (FastAPI + JWT + PKCE)

A complete, standards-compliant OAuth 2.0 Authorization Server implemented in **Python 3.10.11** using **FastAPI**.  
Supports Authorization Code + PKCE flow, RS256-signed JWT access tokens, introspection, revocation, and JWKS key discovery.

---

## Features

- [x] Authorization Code + PKCE flow **RFC 6749 + RFC 7636**
- [x] JWT Access Tokens **RS256**:  fully verifiable, signed with your private RSA key
- [x] User / Client Registration
- [x] Token Introspection (`/oauth/introspect`) **RFC 7662**
- [x] Token Revocation (`/oauth/revoke`) **RFC 7009**
- [x] JWKS Endpoint (`/.well-known/jwks.json`) **RFC 8414 / 7517** for public-key discovery
- [x] Audience, Expiry, Signature Verification for secure API access
- [ ] Refresh token support **RFC 6749**
- [ ] Key rotation with multiple kids **RFC 7517/ 8414**
– [ ] HTTPS / reverse proxy deployment **RFC 6749/ 6819**
- [ ] OpenID Connect (OIDC) metadata (.well-known/openid-configuration) 

---

## Main Components

| Module | Description |
|--------|--------------|
| `app/main.py` | Initializes FastAPI and routers |
| `app/users/` | User registration & model |
| `app/clients/` | OAuth2 client registration |
| `app/auth/` | Authorization, token, introspect, revoke |
| `app/resource/` | Protected API routes |
| `app/security/jwt.py` | RSA key loading & JWT helpers |
| `app/well_known/routes.py` | Publishes JWKS endpoint |
| `keys/` | Contains `private.pem` & `public.pem` |

---

## Get Started

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate RSA keys (if not done)
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem

# 4. Run the server
uvicorn app.main:app --reload
```

# Example Flow

## 1. Register a user
```
curl.exe -X POST "http://127.0.0.1:8000/users/register_user?username=alice&password=secret123"
```

## 2. Register a client
```
curl.exe -X POST "http://127.0.0.1:8000/clients/register_client?client_name=myclient&redirect_uri=http://localhost:8080/callback"
```

## 3. Request authorization code
```
curl.exe -X GET "http://127.0.0.1:8000/oauth/authorize?response_type=code&client_id=<client_id>&redirect_uri=http://localhost:8080/callback&username=alice&password=secret123&state=xyz&code_challenge=dummy123&code_challenge_method=S256"
```

## 4. Exchange code for access token
```
curl.exe -X POST "http://127.0.0.1:8000/oauth/token" `
     -H "Content-Type: application/x-www-form-urlencoded" `
     -d "grant_type=authorization_code&code=<auth_code>&redirect_uri=http://localhost:8080/callback&client_id=<client_id>&code_verifier=dummy123"
```

## 5. Access protected resource
```
curl.exe -H "Authorization: Bearer <access_token>" "http://127.0.0.1:8000/api/profile"
```

## 6. Introspect a token
```
curl.exe -X POST "http://127.0.0.1:8000/oauth/introspect" `
     -H "Content-Type: application/x-www-form-urlencoded" `
     -d "token=<access_token>"
```

## 7. Revoke a token
```
curl.exe -X POST "http://127.0.0.1:8000/oauth/revoke" `
     -H "Content-Type: application/x-www-form-urlencoded" `
     -d "token=<access_token>"
```

## 8. JWKS public key discovery
```
curl.exe -X GET "http://127.0.0.1:8000/.well-known/jwks.json"
```
---
## Token Claims

Example decoded JWT payload:
```
{
  "iss": "http://127.0.0.1:8000",
  "sub": "1",
  "aud": "LnOBKY9x8T_37PXhii0-Kw",
  "scope": "user.read",
  "exp": 1761975556,
  "iat": 1761974656
}
```

# Tech Stack

- FastAPI – API framework
- SQLAlchemy/SQLite – database/models
- python-jose – JWT signing / verification
- cryptography – RSA key handling
- Passlib[bcrypt] – password hashing

# 📜 License

MIT License — feel free to reuse, learn from, or extend this server for your own OAuth2 experiments and integrations.