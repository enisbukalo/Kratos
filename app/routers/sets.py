from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/Set", tags=["Set"])


@router.get("", response_model=list[schemas.ExerciseSet])
async def get_sets(query_params: Annotated[schemas.SetQuery, Depends(schemas.SetQuery)], db: Session = Depends(get_db)):
    query = db.query(models.ExerciseSet)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.ExerciseSet)
async def get_set(id: int = Path(gt=0), db: Session = Depends(get_db)):
    set = db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id).first()
    if set is None:
        raise HTTPException(status_code=404, detail=f"No Set With Id {id} Exists.")

    return set


@router.post("", response_model=schemas.ExerciseSet)
async def create_set(model_to_create: schemas.CreateSet, db: Session = Depends(get_db)):
    created_model = models.ExerciseSet(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return schemas.ExerciseSet.model_validate(created_model)


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

    return set_to_update
