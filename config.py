import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv(
    "DATABASE_NAME",
    "api_employees.db",

)

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "development-jwt-secret-key-change-me-123456",

)

JWT_ALGORITHM = "HS256"

TOKEN_EXPIRE_MINUTES = int(
    os.getenv("TOKEN_EXPIRE_MINUTES", "30")

)

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
]