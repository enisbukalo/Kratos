from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/User", tags=["User"])


@router.get("", response_model=list[schemas.User])
async def get_users(query_params: Annotated[schemas.UserQuery, Depends(schemas.UserQuery)], db: Session = Depends(get_db)):
    query = db.query(models.User)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.User)
async def get_user(id: int = Path(gt=0), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"No User With Id {id} Exists.")

    return user


@router.post("", response_model=schemas.User)
async def create_user(model_to_create: schemas.CreateUser, db: Session = Depends(get_db)):
    created_model = models.User(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return schemas.User.model_validate(created_model)


@router.delete("/{id}")
async def delete_user(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.User)
async def update_user(model_to_update: schemas.CreateUser, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    user_to_update = query.first()

    if user_to_update is None:
        raise HTTPException(status_code=404, detail=f"No User With Id {id} Exists.")

    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(user_to_update)

    return user_to_update
