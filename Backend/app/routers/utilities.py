from fastapi import APIRouter
from sqlalchemy import text

from app import models
from app.database import engine, Base

router = APIRouter(prefix="/Utility", tags=["Utility"])


@router.post("/reset-database")
async def reset_database():
    # Drop all tables
    Base.metadata.drop_all(bind=engine)

    # Recreate all tables
    Base.metadata.create_all(bind=engine)

    return {"message": "Database reset successfully"}
