from sqlalchemy import Column, ForeignKey, Integer, String, FLOAT
from sqlalchemy.orm import relationship

from app.models import BASE, ENGINE

BASE.metadata.create_all(bind=ENGINE)


class Bone(BASE):
    __tablename__ = "bones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    length_cm = Column(FLOAT, nullable=False)

    # Relationships
    skeleton_id = Column(Integer, ForeignKey("skeletons.id", ondelete="CASCADE"), nullable=False, index=True)
    skeleton = relationship("Skeleton", back_populates="bones", uselist=False, cascade="all")
