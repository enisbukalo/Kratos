from sqlalchemy import Column, Integer, DATE, ForeignKey, FLOAT
from sqlalchemy.orm import relationship

from app.models import BASE


class ExerciseSet(BASE):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    reps = Column(Integer, nullable=False)
    weight = Column(FLOAT, nullable=False)
    duration = Column(Integer, nullable=False)  # Duration in seconds
    date = Column(DATE, nullable=False)

    # Relationships
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False, index=True)
    workout = relationship("Workout", back_populates="sets", uselist=False, cascade="all")
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise = relationship("Exercise", uselist=False, cascade="all")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="sets", uselist=False, cascade="all")
