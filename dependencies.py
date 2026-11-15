from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db_session import get_db
from security import decode_access_token
from user_repository import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_username(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db),
) -> str:
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_username(
        session,
        username,
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user.username
