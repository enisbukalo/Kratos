from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db, engine

models.BASE.metadata.create_all(bind=engine)

router = APIRouter(prefix="/Set", tags=["Set"])


@router.get("", response_model=list[schemas.SetReply])
async def get_sets(query_params: Annotated[schemas.SetQuery, Depends(schemas.SetQuery)], db: Session = Depends(get_db)):
    query = db.query(models.ExerciseSet)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.SetReply)
async def get_set(id: int = Path(gt=0), db: Session = Depends(get_db)):
    retrieved_set = db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id).first()
    if retrieved_set is None:
        raise HTTPException(status_code=404, detail=f"No Set With Id {id} Exists.")

    return retrieved_set


@router.post("", response_model=schemas.SetReply)
async def create_set(model_to_create: schemas.CreateSet, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == model_to_create.exercise_id).first()
    if exercise is None:
        raise HTTPException(status_code=404, detail=f"No Exercise With Id {model_to_create.exercise_id} Exists.")
    workout = db.query(models.Workout).filter(models.Workout.id == model_to_create.workout_id).first()
    if workout is None:
        raise HTTPException(status_code=404, detail=f"No Workout With Id {model_to_create.workout_id} Exists.")
    user = db.query(models.User).filter(models.User.id == model_to_create.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"No User With Id {model_to_create.user_id} Exists.")

    created_model = models.ExerciseSet(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return created_model


@router.delete("/{id}")
async def delete_set(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.ExerciseSet)
async def update_set(model_to_update: schemas.CreateSet, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id)
    set_to_update = query.first()

    if set_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Set With Id {id} Exists.")

    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(set_to_update)

    return schemas.ExerciseSet(id=set_to_update.id, reps=set_to_update.reps, date=set_to_update.date)
