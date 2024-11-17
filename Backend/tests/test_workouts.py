import string
import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_workout(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    for workout in generate_workouts:
        assert workout.started_at is not None


def test_get_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    ids = [i.id for i in generate_workouts]

    for id in ids:
        response = client.get(f"/Workout/{id}")
        assert response.status_code == 200
        workout = schemas.WorkoutReply(**response.json())
        assert workout in generate_workouts
        assert workout.started_at is not None

    response = client.get(f"/Workout?page_size=100&page_number=1")
    for workout in response.json():
        workout_obj = schemas.WorkoutReply(**workout)
        assert workout_obj in generate_workouts
        assert workout_obj.started_at is not None


def test_delete_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    for workout in generate_workouts:
        response = client.delete(f"/Workout/{workout.id}")
        assert response.status_code == 200

        response = client.get(f"/Workout/{workout.id}")
        assert response.status_code == 404

    response = client.get(f"/Workout?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    for workout in generate_workouts:
        new_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))

        response = client.put(f"/Workout/{workout.id}", json={"name": new_name})
        assert response.status_code == 200

        updated_workout = schemas.Workout(**response.json())
        assert updated_workout.name == new_name

        # Verify through GET as well
        response = client.get(f"/Workout/{workout.id}")
        assert response.status_code == 200
        get_workout = schemas.WorkoutReply(**response.json())
        assert get_workout.name == new_name


def test_get_latest_workout(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    # Get latest workout
    response = client.get("/Workout?latest=true")
    assert response.status_code == 200
    workouts = [schemas.WorkoutReply(**w) for w in response.json()]
    assert len(workouts) == 1

    # Verify it's the latest one
    latest_workout = workouts[0]
    for workout in generate_workouts:
        response = client.get(f"/Workout/{workout.id}")
        assert response.status_code == 200
        other_workout = schemas.WorkoutReply(**response.json())
        assert latest_workout.started_at >= other_workout.started_at
