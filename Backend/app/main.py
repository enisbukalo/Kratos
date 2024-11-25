from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .routers import exercises, sets, workouts, users, utilities
from .database import get_db
from .models.exercises import DEFAULT_EXERCISES, Exercise


def initialize_exercises(db: Session):
    # Check if exercises table is empty
    existing_exercises = db.query(Exercise).first()
    if existing_exercises is None:
        # Add default exercises
        for exercise in DEFAULT_EXERCISES:
            db.add(Exercise(**exercise))
        db.commit()


def create_app() -> FastAPI:
    origins = ["*"]

    created_app = FastAPI(title="Kratos", version="0.0.1")

    created_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    created_app.include_router(users.router)
    created_app.include_router(workouts.router)
    created_app.include_router(sets.router)
    created_app.include_router(exercises.router)
    created_app.include_router(utilities.router)

    # Initialize database with default exercises
    db = next(get_db())
    initialize_exercises(db)

    return created_app


app = create_app()
