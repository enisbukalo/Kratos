from pydantic import BaseModel, ConfigDict, Field
from typing import List

from app.database import Base, engine

from .query_params import GetQueryParams
from .user_metrics import UserMetricsReply

Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    id: int
    name: str
    height: float
    weight: float


class UserReply(BaseModel):
    id: int
    name: str
    height: float
    weight: float
    workouts: "list[WorkoutReply]"
    metrics: List[UserMetricsReply] = []


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    name: str = Field(default="First Last", min_length=4, max_length=100)
    height: float = Field(default=64, gt=0)
    weight: float = Field(default=225.6, gt=0)


class UserQuery(GetQueryParams):
    pass


from .workouts import WorkoutReply

WorkoutReply.model_rebuild()
