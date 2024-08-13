from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/Skeleton", tags=["Skeleton"])


@router.get("", response_model=list[schemas.Skeleton])
async def get_skeletons(query_params: Annotated[schemas.SkeletonsQuery, Depends(schemas.SkeletonsQuery)], db: Session = Depends(get_db)):
    query = db.query(models.Skeleton)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.Skeleton)
async def get_skeleton(id: int = Path(gt=0), db: Session = Depends(get_db)):
    skeleton = db.query(models.Skeleton).filter(models.Skeleton.id == id).first()
    if skeleton is None:
        raise HTTPException(status_code=404, detail=f"No Skeleton With Id {id} Exists.")

    return skeleton


@router.post("", response_model=schemas.Skeleton)
async def create_skeleton(skeleton_to_create: schemas.CreateSkeleton, db: Session = Depends(get_db)):
    created_skeleton = models.Skeleton(**skeleton_to_create.model_dump())

    db.add(created_skeleton)
    db.commit()
    db.refresh(created_skeleton)

    return schemas.Skeleton.model_validate(created_skeleton)


@router.delete("/{id}")
async def delete_skeleton(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Skeleton).filter(models.Skeleton.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Skeleton)
async def update_skeleton(skeleton_updates: schemas.CreateSkeleton, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Skeleton).filter(models.Skeleton.id == id)
    skeleton_to_update = query.first()

    if skeleton_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Skeleton With Id {id} Exists.")

    query.update(skeleton_updates.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(skeleton_to_update)

    return skeleton_to_update
