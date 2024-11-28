from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from datetime import date as _date

from app.database import Base, engine

from .query_params import GetQueryParams


Base.metadata.create_all(bind=engine)


class SetBase(BaseModel):
    id: int
    reps: int
    weight: float
    duration: int  # Duration in seconds
    distance: float
    date: _date
    exercise: "Exercise"


class SetReply(BaseModel):
    id: int
    reps: int
    weight: float
    duration: int  # Duration in seconds
    distance: float
    date: _date
    workout: "Workout"
    exercise: "Exercise"
    user: "User"


class ExerciseSet(SetBase):
    model_config = ConfigDict(from_attributes=True)


class CreateSet(BaseModel):
    reps: int = Field(default=5, ge=0)
    weight: float = Field(default=0.0, ge=0.0)
    duration: int = Field(default=0, ge=0)  # Duration in seconds
    distance: float = Field(default=0.0, ge=0.0)
    date: _date = Field(default=_date.today())
    exercise_id: PositiveInt
    workout_id: PositiveInt
    user_id: PositiveInt


class MultiSets(BaseModel):
    reps: int = Field(default=5, ge=0)
    weight: float = Field(default=0.0, ge=0.0)
    duration: int = Field(default=0, ge=0)  # Duration in seconds
    distance: float = Field(default=0.0, ge=0.0)
    date: _date = Field(default=_date.today())


class CreateSets(BaseModel):
    exercise_id: PositiveInt
    workout_id: PositiveInt
    user_id: PositiveInt
    sets: list[MultiSets]


class UpdateSet(BaseModel):
    id: int
    reps: int | None = None
    weight: float | None = None
    duration: int | None = None
    distance: float | None = None
    date: _date | None = None


class BulkUpdateSets(BaseModel):
    exercise_id: PositiveInt
    workout_id: PositiveInt
    user_id: PositiveInt
    sets: list[UpdateSet]


class SetQuery(GetQueryParams):
    pass


from .workouts import Workout
from .users import User
from .exercises import Exercise

Workout.model_rebuild()
User.model_rebuild()
Exercise.model_rebuild()
