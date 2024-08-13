from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models import BASE


class Workout(BASE):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", back_populates="workouts", uselist=False, cascade="all")
    sets = relationship("ExerciseSet", back_populates="workout", uselist=True, cascade="all")
