from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.database import Base, engine

from .query_params import GetQueryParams
from .sets import ExerciseSet

Base.metadata.create_all(bind=engine)


class WorkoutBase(BaseModel):
    id: int
    name: str


class WorkoutReply(BaseModel):
    id: int
    name: str
    sets: "list[ExerciseSet]"


class Workout(WorkoutBase):
    model_config = ConfigDict(from_attributes=True)


class CreateWorkout(BaseModel):
    name: str = Field(default="Workout Name", min_length=4, max_length=100)
    user_id: PositiveInt


class WorkoutQuery(GetQueryParams):
    pass


from .bone import Bone

Bone.model_rebuild()
