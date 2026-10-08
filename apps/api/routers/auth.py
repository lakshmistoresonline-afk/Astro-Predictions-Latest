"""
User Registration, Login, Logout, and Authentication Router for Astrovision.
Exposes user signup, login token issuance, logout session revocation, and authenticated user profile routes.
"""
from fastapi import APIRouter, HTTPException, Depends, Header, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session
from typing import Optional

from apps.api.config import settings
from apps.api.db.database import get_db
from apps.api.db.models import UserModel
from apps.api.db.auth import (
    hash_password,
    verify_password,
    create_access_token,
    revoke_token,
    get_current_user
)
from apps.api.exceptions import (
    AstrovisionValidationError,
    AuthenticationError,
    ResourceConflictError
)

router = APIRouter(prefix="/api/v1/auth", tags=["User Authentication"])

class UserRegisterRequest(BaseModel):
    email: str = Field(description="User's unique email address")
    password: str = Field(min_length=8, description="Password (minimum 8 characters)")
    full_name: str = Field(min_length=1, description="User's full name")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if "@" not in v_clean or "." not in v_clean:
            raise ValueError("Invalid email address format.")
        return v_clean

class UserLoginRequest(BaseModel):
    email: str = Field(description="User's registered email address")
    password: str = Field(description="User's plain password")

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        v_clean = v.strip().lower()
        if "@" not in v_clean or "." not in v_clean:
            raise ValueError("Invalid email address format.")
        return v_clean

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_hours: int
    user_id: str
    email: str
    full_name: str

class UserProfileResponse(BaseModel):
    id: str
    email: str
    full_name: str
    created_at: str

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
def register_user(req: UserRegisterRequest, db: Session = Depends(get_db)):
    """Registers a new user account with salted PBKDF2-HMAC-SHA256 password hashing."""
    clean_email = req.email.strip().lower()

    existing = db.query(UserModel).filter(UserModel.email == clean_email).first()
    if existing:
        raise ResourceConflictError(f"User account with email '{clean_email}' already exists.")

    hashed_pw, salt_hex = hash_password(req.password)

    user = UserModel(
        email=clean_email,
        hashed_password=hashed_pw,
        password_salt=salt_hex,
        full_name=req.full_name.strip()
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_hours=settings.jwt_expiration_hours,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name
    )

@router.post("/login", response_model=TokenResponse)
def login_user(req: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticates user credentials and issues a cryptographically signed JWT access token."""
    clean_email = req.email.strip().lower()

    user = db.query(UserModel).filter(UserModel.email == clean_email).first()
    if not user:
        raise AuthenticationError("Invalid email or password.")

    if not user.password_salt:
        raise AuthenticationError("Invalid email or password.")

    if not verify_password(req.password, user.hashed_password, user.password_salt):
        raise AuthenticationError("Invalid email or password.")

    token = create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_hours=settings.jwt_expiration_hours,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name
    )

@router.post("/logout")
def logout_user(
    authorization: Optional[str] = Header(None),
    current_user: UserModel = Depends(get_current_user)
):
    """Revokes active Bearer JWT token session and registers token in revocation registry."""
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
        revoke_token(token)

    return {"status": "logged_out", "message": "Successfully logged out and session token revoked."}

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(current_user: UserModel = Depends(get_current_user)):
    """Retrieves authenticated user profile information for the current token context."""
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at.isoformat()
    )

@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_my_account(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Deletes the authenticated user's account and all associated private resources
    (birth profiles, saved charts, reports, AI records, quota logs) cleanly.
    """
    user_id = current_user.id
    email = current_user.email

    from apps.api.db.models import UserQuotaModel
    db.query(UserQuotaModel).filter(UserQuotaModel.identifier == user_id).delete(synchronize_session=False)

    db.delete(current_user)
    db.commit()

    return {"status": "success", "message": f"Account '{email}' and all associated private data permanently deleted."}
