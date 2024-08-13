from sqlalchemy import Column, Integer, String

from app.database import Base, engine

Base.metadata.create_all(bind=engine)


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
