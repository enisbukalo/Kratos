from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status
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

    # Ensure set exists.
    if retrieved_set is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Set With Id {id} Exists.")

    return retrieved_set


@router.post("", response_model=schemas.SetReply)
async def create_set(model_to_create: schemas.CreateSet, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == model_to_create.exercise_id).first()

    # Ensure exercise exists.
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Exercise With Id {model_to_create.exercise_id} Exists.")

    # Ensure workout exists.
    workout = db.query(models.Workout).filter(models.Workout.id == model_to_create.workout_id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {model_to_create.workout_id} Exists.")

    # Ensure user exists.
    user = db.query(models.User).filter(models.User.id == model_to_create.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No User With Id {model_to_create.user_id} Exists.")

    created_model = models.ExerciseSet(**model_to_create.model_dump())

    db.add(created_model)
    db.commit()
    db.refresh(created_model)

    return created_model


@router.post("/bulk", response_model=list[schemas.SetReply])
async def create_sets(models_to_create: schemas.CreateSets, db: Session = Depends(get_db)):
    created_sets = []

    # Validate exercise exists - do this once for all sets
    exercise = db.query(models.Exercise).filter(models.Exercise.id == models_to_create.exercise_id).first()
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Exercise With Id {models_to_create.exercise_id} Exists.")

    # Validate workout exists - do this once for all sets
    workout = db.query(models.Workout).filter(models.Workout.id == models_to_create.workout_id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {models_to_create.workout_id} Exists.")

    # Validate user exists - do this once for all sets
    user = db.query(models.User).filter(models.User.id == models_to_create.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No User With Id {models_to_create.user_id} Exists.")

    for set_data in models_to_create.sets:
        # Combine the set-specific data with the common IDs
        set_dict = set_data.model_dump()
        set_dict.update({"exercise_id": models_to_create.exercise_id, "workout_id": models_to_create.workout_id, "user_id": models_to_create.user_id})

        created_model = models.ExerciseSet(**set_dict)
        db.add(created_model)
        created_sets.append(created_model)

    db.commit()
    for set_model in created_sets:
        db.refresh(set_model)

    return created_sets


@router.delete("/{id}")
async def delete_set(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id).delete()
    db.commit()


@router.put("/bulk", response_model=list[schemas.SetReply])
async def update_sets(models_to_update: schemas.BulkUpdateSets, db: Session = Depends(get_db)):
    updated_sets = []

    # Validate exercise exists - do this once for all sets
    exercise = db.query(models.Exercise).filter(models.Exercise.id == models_to_update.exercise_id).first()
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Exercise With Id {models_to_update.exercise_id} Exists.")

    # Validate workout exists - do this once for all sets
    workout = db.query(models.Workout).filter(models.Workout.id == models_to_update.workout_id).first()
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {models_to_update.workout_id} Exists.")

    # Validate user exists - do this once for all sets
    user = db.query(models.User).filter(models.User.id == models_to_update.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No User With Id {models_to_update.user_id} Exists.")

    for set_data in models_to_update.sets:
        # Get the set to update
        query = db.query(models.ExerciseSet).filter(models.ExerciseSet.id == set_data.id)
        set_to_update = query.first()

        # Ensure set exists
        if set_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Set With Id {set_data.id} Exists.")

        # Combine the set-specific data with the common IDs
        set_dict = set_data.model_dump()
        set_dict.update({"exercise_id": models_to_update.exercise_id, "workout_id": models_to_update.workout_id, "user_id": models_to_update.user_id})

        # Update the set
        query.update(set_dict, synchronize_session=False)
        updated_sets.append(set_to_update)

    db.commit()
    for set_model in updated_sets:
        db.refresh(set_model)

    return updated_sets


@router.put("/{id}", response_model=schemas.ExerciseSet)
async def update_set(model_to_update: schemas.CreateSet, id: int = Path(gt=0), db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == model_to_update.exercise_id).first()

    # Ensure exercise exists.
    if exercise is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Exercise With Id {model_to_update.exercise_id} Exists.")

    workout = db.query(models.Workout).filter(models.Workout.id == model_to_update.workout_id).first()

    # Ensure workout exists.
    if workout is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {model_to_update.workout_id} Exists.")
    user = db.query(models.User).filter(models.User.id == model_to_update.user_id).first()

    # Ensure user exists.
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No User With Id {model_to_update.user_id} Exists.")

    query = db.query(models.ExerciseSet).filter(models.ExerciseSet.id == id)
    set_to_update = query.first()

    # Ensure set exists.
    if set_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Set With Id {id} Exists.")

    query.update(model_to_update.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(set_to_update)

    return schemas.ExerciseSet(
        id=set_to_update.id,
        reps=set_to_update.reps,
        weight=set_to_update.weight,
        duration=set_to_update.duration,
        distance=set_to_update.distance,
        date=set_to_update.date,
        exercise=exercise,
    )


@router.delete("/empty", response_model=dict)
async def delete_empty_sets(db: Session = Depends(get_db)):
    """Delete all sets that have empty/zero values for all metrics (reps, weight, duration, and distance)"""
    # Delete sets where all metrics are empty/zero
    query = db.query(models.ExerciseSet).filter(
        models.ExerciseSet.reps == 0, models.ExerciseSet.weight == 0, models.ExerciseSet.duration == 0, models.ExerciseSet.distance == 0
    )

    # Get the count of sets to be deleted
    sets_to_delete = query.count()

    # Delete the sets
    query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"Successfully deleted {sets_to_delete} empty sets", "deleted_count": sets_to_delete}
