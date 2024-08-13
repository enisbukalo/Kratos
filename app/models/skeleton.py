from sqlalchemy import Column, Integer, String, FLOAT
from sqlalchemy.orm import relationship

from app.database import Base, engine

Base.metadata.create_all(bind=engine)


class Skeleton(Base):
    __tablename__ = "skeletons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    height_m = Column(FLOAT, nullable=False)

    # Relationships
    bones = relationship("Bone", back_populates="skeleton", uselist=True, cascade="all")
