from dotenv import load_dotenv
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from schemas.token_schema import TokenData
from jwt.exceptions import InvalidTokenError
import os
import jwt

load_dotenv() # load environment variables

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = os.environ.get("JWT_SECRET")
ALGORITHM = os.environ.get("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=60

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if plain and hashed password is the same."""

    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash plain password and return hashed password."""

    return password_hash.hash(password)


def create_access_token(data: dict) -> str:
    """create access token using jwt, and return it."""

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), ) -> TokenData:
    """Verify access token and get user data."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        pay_load = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = pay_load.get("user_id")
        username: str = pay_load.get("username")

        if username is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=user_id, username=username)
    except InvalidTokenError:
        raise credentials_exception

    return token_data