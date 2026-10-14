from fastapi import APIRouter, HTTPException

from database import check_database_connection

router = APIRouter(tags=["system"])

@router.get("/health")
def health_check():
    if not check_database_connection():
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )

    return {
        "status": "ok",
        "database": "connected",
    }