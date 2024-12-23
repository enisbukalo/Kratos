from typing_extensions import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db, engine

models.BASE.metadata.create_all(bind=engine)

router = APIRouter(prefix="/Workout", tags=["Workout"])


@router.get("/workouts/", response_model=list[schemas.WorkoutReply])
async def get_workouts(query_params: Annotated[schemas.GetQueryParams, Depends(schemas.GetQueryParams)], db: Session = Depends(get_db)):
    query = db.query(models.Workout)

    return (
        query.order_by(models.Workout.started_at.desc())
        .limit(query_params.page_size)
        .offset((query_params.page_number * query_params.page_size) if query_params.page_number > 1 else 0)
        .all()
    )


@router.get("/workouts/{user_id}", response_model=list[schemas.WorkoutReply])
async def get_latest_workouts_for_user(user_id: int = Path(gt=0), db: Session = Depends(get_db)):
    query = db.query(models.Workout)

    # Get all of the workouts for this user.
    query = query.filter(models.Workout.user_id == user_id)

    # Parse all of the workouts for uniquely named workouts.
    unique_workouts = {workout.name: workout for workout in query.all()}

    # Query the database for the latest workout for each unique named workout.
    return list(unique_workouts.values())


@router.get("/{id}", response_model=schemas.WorkoutReply)
async def get_workout(id: int = Path(gt=0), db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(models.Workout.id == id).first()
    if workout is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {id} Exists.")

    return workout


@router.post("", response_model=schemas.WorkoutReply)
async def create_workout(model_to_create: schemas.CreateWorkout, db: Session = Depends(get_db)):
    created_model = models.Workout(**model_to_create.model_dump())
    db.add(created_model)
    db.commit()
    db.refresh(created_model)
    return created_model


@router.delete("/{id}")
async def delete_workout(id: int = Path(gt=0), db: Session = Depends(get_db)):
    db.query(models.Workout).filter(models.Workout.id == id).delete()
    db.commit()


@router.put("/{id}", response_model=schemas.Workout)
async def update_workout(model_to_update: schemas.UpdateWorkout, id: int = Path(gt=0), db: Session = Depends(get_db)):
    # Query the database for the workout to update.
    query = db.query(models.Workout).filter(models.Workout.id == id)
    workout_to_update = query.first()

    # Ensure that the workout exists.
    if workout_to_update is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"No Workout With Id {id} Exists.")

    # Exclude any unset fields from the update data.
    workout_to_update.name = model_to_update.name
    db.commit()
    db.refresh(workout_to_update)

    return workout_to_update
