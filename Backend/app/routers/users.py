from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app import models, schemas
from app.database import get_db, engine

models.BASE.metadata.create_all(bind=engine)

router = APIRouter(prefix="/User", tags=["User"])


@router.get("", response_model=list[schemas.UserReply])
async def get_users(query_params: Annotated[schemas.UserQuery, Depends(schemas.UserQuery)], db: Session = Depends(get_db)):
    query = db.query(models.User)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.UserReply)
async def get_user(id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"No User With Id {id} Exists.")

    return user


@router.post("", response_model=schemas.UserReply)
async def create_user(model_to_create: schemas.CreateUser, db: Session = Depends(get_db)):
    created_model = models.User(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    # Create a new user metric for the user.
    new_user_metric = models.UserMetrics(
        user_id=created_model.id, weight=created_model.weight, height=created_model.height, recorded_at=datetime.now()
    )
    db.add(new_user_metric)
    db.commit()

    return created_model


@router.delete("/{id}")
async def delete_user(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete()
    db.query(models.UserMetrics).filter(models.UserMetrics.user_id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.User)
async def update_user(model_to_update: schemas.CreateUser, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    user_to_update = query.first()

    # Ensure that the user exists.
    if user_to_update is None:
        raise HTTPException(status_code=404, detail=f"No User With Id {id} Exists.")

    # Update the user with the new data.
    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(user_to_update)

    return user_to_update


@router.post("/{user_id}/metrics", response_model=schemas.UserMetricsReply)
async def create_user_metrics(user_id: int = Path(gt=0), metrics: schemas.UserMetricsCreate = None, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    # Ensure that the user exists.
    if not user:
        raise HTTPException(status_code=404, detail=f"No User With Id {user_id} Exists.")

    # Create a new user metric for the user.
    db_metrics = models.UserMetrics(user_id=user_id, weight=metrics.weight, height=metrics.height, recorded_at=datetime.now())

    db.add(db_metrics)
    db.commit()
    db.refresh(db_metrics)

    return db_metrics


@router.get("/{user_id}/metrics", response_model=List[schemas.UserMetricsReply])
async def get_user_metrics(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    metrics = db.query(models.UserMetrics).filter(models.UserMetrics.user_id == user_id).order_by(models.UserMetrics.recorded_at.desc()).all()
    return metrics
