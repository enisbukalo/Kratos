from sqlalchemy import Column, Integer, String, FLOAT
from sqlalchemy.orm import relationship

from app.models import BASE


class User(BASE):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    height = Column(FLOAT, nullable=False)
    weight = Column(FLOAT, nullable=False)

    # Relationships
    workouts = relationship("Workout", back_populates="user", uselist=True, cascade="all")
    sets = relationship("ExerciseSet", back_populates="user", uselist=True, cascade="all")
