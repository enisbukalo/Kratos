from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from datetime import datetime

from app.database import Base, engine

from .query_params import GetQueryParams

Base.metadata.create_all(bind=engine)


class WorkoutBase(BaseModel):
    id: int
    name: str
    started_at: datetime | None = None


class WorkoutReply(BaseModel):
    id: int
    name: str
    started_at: datetime | None = None
    sets: "list[ExerciseSet]"


class Workout(WorkoutBase):
    model_config = ConfigDict(from_attributes=True)


class CreateWorkout(BaseModel):
    name: str = Field(default="Workout Name", min_length=4, max_length=100)
    user_id: PositiveInt


class UpdateWorkout(BaseModel):
    name: str | None = None
    started_at: datetime | None = None


class WorkoutQuery(GetQueryParams):
    pass


from .sets import ExerciseSet
from .users import User

ExerciseSet.model_rebuild()
User.model_rebuild()
