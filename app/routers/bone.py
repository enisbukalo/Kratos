from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/Bone", tags=["Bone"])


@router.get("", response_model=list[schemas.Bone])
async def get_bones(query_params: Annotated[schemas.BonesQuery, Depends(schemas.BonesQuery)], db: Session = Depends(get_db)):
    query = db.query(models.Bone)

    return query.limit(query_params.page_size).offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0).all()


@router.get("/{id}", response_model=schemas.Bone)
async def get_bone(id: int = Path(gt=0), db: Session = Depends(get_db)):
    Bone = db.query(models.Bone).filter(models.Bone.id == id).first()
    if Bone is None:
        raise HTTPException(status_code=404, detail=f"No Bone With Id {id} Exists.")

    return Bone


@router.post("", response_model=schemas.Bone)
async def create_bone(bone_to_create: schemas.CreateBone, db: Session = Depends(get_db)):
    created_Bone = models.Bone(**bone_to_create.model_dump())

    db.add(created_Bone)
    db.commit()
    db.refresh(created_Bone)

    return schemas.Bone.model_validate(created_Bone)


@router.delete("/{id}")
async def delete_bone(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Bone).filter(models.Bone.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Bone)
async def update_bone(bone_updates: schemas.CreateBone, id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Bone).filter(models.Bone.id == id)
    Bone_to_update = query.first()

    if Bone_to_update is None:
        raise HTTPException(status_code=404, detail=f"No Bone With Id {id} Exists.")

    query.update(bone_updates.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(Bone_to_update)

    return Bone_to_update
