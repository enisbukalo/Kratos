from sqlalchemy import Column, Integer, String, FLOAT
from sqlalchemy.orm import relationship

from app.database import Base, engine

Base.metadata.create_all(bind=engine)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    height = Column(FLOAT, nullable=False)
    weight = Column(FLOAT, nullable=False)

    # Relationships
    workouts = relationship("Workout", uselist=True, cascade="all")
    sets = relationship("ExerciseSet", uselist=True, cascade="all")
