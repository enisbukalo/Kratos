from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/Workout", tags=["Workout"])


@router.get("", response_model=list[schemas.Workout])
async def get_workouts(query_params: Annotated[schemas.WorkoutQuery, Depends(schemas.WorkoutQuery)], db: Session = Depends(get_db)):
    query = db.query(models.Workout)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.Workout)
async def get_workout(id: int = Path(gt=0), db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail=f"No Workout With Id {id} Exists.")

    return workout


@router.post("", response_model=schemas.Workout)
async def create_workout(model_to_create: schemas.CreateWorkout, db: Session = Depends(get_db)):
    created_model = models.Workout(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return schemas.Workout.model_validate(created_model)


@router.delete("/{id}")
async def delete_workout(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Workout).filter(models.Workout.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Workout)
async def update_workout(model_to_update: schemas.CreateWorkout, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Workout).filter(models.Workout.id == id)
    workout_to_update = query.first()

    if workout_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Workout With Id {id} Exists.")

    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(workout_to_update)

    return workout_to_update
