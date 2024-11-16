from sqlalchemy import Column, Integer, String

from app.models import BASE


class Exercise(BASE):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


DEFAULT_EXERCISES = [
    "Bench Press",
    "Squat",
    "Deadlift",
    "Overhead Press",
    "Barbell Row",
    "Pull Up",
    "Push Up",
    "Dip",
    "Lunge",
    "Plank",
]
