from pydantic import BaseModel, ConfigDict, Field

from app.database import Base, engine

from .query_params import GetQueryParams
from .workouts import Workout

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
    workouts: "list[Workout]"


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    name: str = Field(default="First Last", min_length=4, max_length=100)
    height: float = Field(default=64, gt=0)
    weight: float = Field(default=225.6, gt=0)


class UserQuery(GetQueryParams):
    pass


from .bone import Bone

Bone.model_rebuild()
