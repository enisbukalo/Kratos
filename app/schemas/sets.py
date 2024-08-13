from pydantic import BaseModel, ConfigDict, Field
from datetime import date as _date

from app.database import Base, engine

from .query_params import GetQueryParams
from .workouts import Workout
from .users import User
from .exercises import Exercise

Base.metadata.create_all(bind=engine)


class SetBase(BaseModel):
    id: int
    reps: int
    date: _date


class SetReply(BaseModel):
    id: int
    reps: int
    date: _date
    workout: "Workout"
    exercise: "Exercise"
    user: "User"


class ExerciseSet(SetBase):
    model_config = ConfigDict(from_attributes=True)


class CreateSet(BaseModel):
    reps: int = Field(default=5, gt=0)
    date: _date = Field(default=_date.today())


class SetQuery(GetQueryParams):
    pass


from .bone import Bone

Bone.model_rebuild()
