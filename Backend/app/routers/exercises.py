from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db, engine

models.BASE.metadata.create_all(bind=engine)

router = APIRouter(prefix="/Exercise", tags=["Exercise"])


@router.get("", response_model=list[schemas.Exercise])
async def get_exercises(query_params: Annotated[schemas.ExerciseQuery, Depends(schemas.ExerciseQuery)], db: Session = Depends(get_db)):
    query = db.query(models.Exercise)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.Exercise)
async def get_exercise(id: int = Path(gt=0), db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if exercise is None:
        raise HTTPException(status_code=404, detail=f"No Exercise With Id {id} Exists.")

    return exercise


@router.post("", response_model=schemas.Exercise)
async def create_exercise(model_to_create: schemas.CreateExercise, db: Session = Depends(get_db)):
    created_model = models.Exercise(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return schemas.Exercise.model_validate(created_model)


@router.delete("/{id}")
async def delete_exercise(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Exercise).filter(models.Exercise.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Exercise)
async def update_exercise(model_to_update: schemas.CreateExercise, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Exercise).filter(models.Exercise.id == id)
    exercise_to_update = query.first()

    if exercise_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Exercise With Id {id} Exists.")

    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(exercise_to_update)

    return exercise_to_update
