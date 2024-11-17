from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from datetime import datetime

from app.database import Base, engine

from .query_params import GetQueryParams

Base.metadata.create_all(bind=engine)


class WorkoutBase(BaseModel):
    id: int
    name: str
    started_at: datetime


class WorkoutReply(BaseModel):
    id: int
    name: str
    started_at: datetime
    sets: "list[ExerciseSet]"


class Workout(WorkoutBase):
    model_config = ConfigDict(from_attributes=True)


class CreateWorkout(BaseModel):
    name: str = Field(default="Workout Name", min_length=4, max_length=100)
    user_id: PositiveInt
    started_at: datetime = Field(default_factory=datetime.now)


class UpdateWorkout(BaseModel):
    name: str | None = None


class WorkoutQuery(GetQueryParams):
    latest: bool = Field(default=False, description="Get only the latest workout by started_at")


from .sets import ExerciseSet
from .users import User

ExerciseSet.model_rebuild()
User.model_rebuild()
