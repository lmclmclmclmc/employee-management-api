from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from database import create_user, get_user_by_username
from dependencies import get_current_username
from schemas import TokenResponse, UserCreate, UserResponse
from security import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(tags=["authentication"])

@router.get("/me")
def read_current_user(
    username: str = Depends(get_current_username),
):
    return {"username": username}

@router.post(
    "/register",
    status_code=201,
    response_model=UserResponse,
)
def register(user: UserCreate):
    password_hash = hash_password(user.password)

    created_user = create_user(
        user.username,
        password_hash,
    )

    if created_user is None:
        raise HTTPException(
            status_code=409,
            detail="Username already exists",
        )

    return created_user

@router.post(
    "/login",
    response_model=TokenResponse,

)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),

):
    user = get_user_by_username(form_data.username)

    if user is None or not verify_password(
        form_data.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(user["username"])

    return {
        "access_token": token,
        "token_type": "bearer",
    }