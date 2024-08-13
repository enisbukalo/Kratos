from sqlalchemy import Column, Integer, DATE, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base, engine

Base.metadata.create_all(bind=engine)


class ExerciseSet(Base):
    __tablename__ = "sets"

    id = Column(Integer, primary_key=True, index=True)
    reps = Column(Integer, nullable=False)
    date = Column(DATE, nullable=False)

    # Relationships
    workout_id = Column(Integer, ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False, index=True)
    exercises = relationship("Exercise", uselist=True, cascade="all")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    user = relationship("User", uselist=False, cascade="all")
