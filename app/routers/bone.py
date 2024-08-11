from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db, engine

models.BASE.metadata.create_all(bind=engine)
router = APIRouter(prefix="/Bone", tags=["Bone"])


@router.get("", response_model=list[schemas.Bone])
async def get_bones(query_params: Annotated[schemas.BonesQuery, Depends(schemas.BonesQuery)], db: Session = Depends(get_db)):
    query = db.query(models.Bone)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.Bone)
async def get_bone(id: int = Path(gt=0), db: Session = Depends(get_db)):
    bone = db.query(models.Bone).filter(models.Bone.id == id).first()
    if bone is None:
        raise HTTPException(status_code=404, detail=f"No Bone With Id {id} Exists.")

    return bone


@router.post("", response_model=schemas.Bone)
async def create_bone(bone_to_create: schemas.CreateBone, db: Session = Depends(get_db)):
    created_bone = models.Bone(**bone_to_create.model_dump())

    db.add(created_bone)
    db.commit()
    db.refresh(created_bone)

    return schemas.Bone.model_validate(created_bone)


@router.delete("/{id}")
async def delete_bone(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Bone).filter(models.Bone.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Bone)
async def update_bone(bone_updates: schemas.CreateBone, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Bone).filter(models.Bone.id == id)
    bone_to_update = query.first()

    if bone_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Bone With Id {id} Exists.")

    query.update(bone_updates.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(bone_to_update)

    return bone_to_update
