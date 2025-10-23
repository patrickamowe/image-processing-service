from sqlalchemy.orm import Session
from models.models import User
from schemas.token_schema import Token
from utils.auth_utils import verify_password, create_access_token
from db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login_user(
        user_credential: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """Login user and create access token."""

    user = db.query(User).filter(User.username==user_credential.username).first()

    #Ensure username is unique
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Username already taken."
        )

    if not verify_password(user_credential.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credential."
        )

    data = {"user_id":user.id, "username": user.username}
    access_token = create_access_token(data)
    return Token(access_token=access_token, token_type="bearer")