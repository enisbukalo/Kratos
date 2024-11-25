from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models import BASE


class UserMetrics(BASE):
    __tablename__ = "user_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    weight = Column(Float)
    height = Column(Float)
    recorded_at = Column(DateTime, default=datetime.now)

    # Relationship
    user = relationship("User", back_populates="metrics")
