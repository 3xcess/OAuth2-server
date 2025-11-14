from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    scopes = Column(String, default="user.read")
    created_at = Column(DateTime, default=datetime.utcnow)

class OAuthClient(Base):
    __tablename__ = "oauth_clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, nullable=False)
    client_secret = Column(String, nullable=True)  # public clients can have None
    redirect_uris = Column(String, nullable=False)  # comma-separated list
    allowed_scopes = Column(String, default="user.read")
    is_confidential = Column(Boolean, default=True)


class AuthCode(Base):
    __tablename__ = "auth_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    client_id = Column(String, nullable=False)
    redirect_uri = Column(String, nullable=False)
    code_challenge = Column(String, nullable=True)
    code_challenge_method = Column(String, default="S256")
    scope = Column(String, default="user.read")
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User")