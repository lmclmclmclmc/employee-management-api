from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from config import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    TOKEN_EXPIRE_MINUTES,
)

password_hash = PasswordHash.recommended()


def create_access_token(username):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    payload = {"sub": username, "exp": expires_at}

    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_access_token(token):
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.InvalidTokenError:
        return None


def hash_password(password):
    return password_hash.hash(password)


def verify_password(password, hashed_password):
    return password_hash.verify(password, hashed_password)


if __name__ == "__main__":
    hashed = hash_password("my-secret-password")

    print(f"hashed : {hashed}")
    print(verify_password("my-secret-password", hashed))
    print(verify_password("wrong-password", hashed))

    token = create_access_token("admin")
    print(token)
    print(decode_access_token(token))
    print(decode_access_token("invalid-token"))
