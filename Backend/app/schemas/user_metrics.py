from datetime import datetime
from pydantic import BaseModel, Field


class UserMetricsBase(BaseModel):
    weight: float = Field(gt=0, description="User's weight in kilograms")
    height: float = Field(gt=0, description="User's height in centimeters")


class UserMetricsCreate(UserMetricsBase):
    pass


class UserMetricsReply(UserMetricsBase):
    id: int
    user_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True
