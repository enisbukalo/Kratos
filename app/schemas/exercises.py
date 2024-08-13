from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from app.database import Base, engine

from .query_params import GetQueryParams

Base.metadata.create_all(bind=engine)


class ExerciseBase(BaseModel):
    id: int
    name: str


class ExerciseReply(BaseModel):
    id: int
    name: str


class Exercise(ExerciseBase):
    model_config = ConfigDict(from_attributes=True)


class CreateExercise(BaseModel):
    name: str = Field(default="Exercise Name", min_length=4, max_length=100)
    user_id: PositiveInt


class ExerciseQuery(GetQueryParams):
    pass


from .bone import Bone

Bone.model_rebuild()
