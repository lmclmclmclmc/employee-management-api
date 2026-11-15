from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db_session import get_db

router = APIRouter(tags=["system"])


@router.get("/health")
def health_check(
    session: Session = Depends(get_db),
):
    try:
        session.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        ) from error

    return {
        "status": "ok",
        "database": "connected",
    }
