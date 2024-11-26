import string
import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 24


def test_create_workout(client: TestClient, generate_users: list[schemas.UserReply]):
    user = generate_users[0]
    workout_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))
    started_at = datetime.now()

    response = client.post("/Workout", json={"name": workout_name, "user_id": user.id, "started_at": started_at.isoformat()})

    assert response.status_code == 200
    workout = schemas.WorkoutReply(**response.json())
    assert workout.name == workout_name
    assert workout.started_at is not None


def test_get_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    # Get all workouts with pagination
    response = client.get(f"/Workout/workouts/?page_size=100&page_number=1")
    assert response.status_code == 200
    workouts = [schemas.WorkoutReply(**w) for w in response.json()]
    assert len(workouts) > 0


def test_get_workout_by_id(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    workout = random.choice(generate_workouts)
    response = client.get(f"/Workout/{workout.id}")
    assert response.status_code == 200
    fetched_workout = schemas.WorkoutReply(**response.json())
    assert fetched_workout.id == workout.id
    assert fetched_workout.name == workout.name


def test_get_workout_not_found(client: TestClient):
    response = client.get("/Workout/999999")
    assert response.status_code == 404


def test_update_workout(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    workout = generate_workouts[0]
    new_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))

    response = client.put(f"/Workout/{workout.id}", json={"name": new_name})
    assert response.status_code == 200
    updated_workout = schemas.Workout(**response.json())
    assert updated_workout.name == new_name


def test_delete_workout(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    workout = generate_workouts[0]

    # Delete workout
    response = client.delete(f"/Workout/{workout.id}")
    assert response.status_code == 200

    # Verify it's deleted
    response = client.get(f"/Workout/{workout.id}")
    assert response.status_code == 404


def test_get_latest_workouts_for_user(client: TestClient, generate_users: list[schemas.UserReply]):
    user = random.choice(generate_users)

    # Create multiple workouts with same names at different times
    workout_data = [
        ("Workout A", datetime.now() - timedelta(days=2)),
        ("Workout B", datetime.now() - timedelta(days=1)),
        ("Workout A", datetime.now()),  # Latest "Workout A"
    ]

    created_workouts = []
    for name, started_at in workout_data:
        response = client.post("/Workout", json={"name": name, "user_id": user.id, "started_at": started_at.isoformat()})
        assert response.status_code == 200
        created_workouts.append(schemas.WorkoutReply(**response.json()))

    # Get latest workouts
    response = client.get(f"/Workout/workouts/{user.id}?user_id={user.id}")
    assert response.status_code == 200
    latest_workouts = [schemas.WorkoutReply(**w) for w in response.json()]

    # Should get 2 workouts (latest of each name)
    assert len(latest_workouts) == 2

    # Create dict of workouts by name
    workout_dict = {w.name: w for w in latest_workouts}

    # Verify we got the latest "Workout A"
    assert workout_dict["Workout A"].started_at == created_workouts[2].started_at

    # Verify we got "Workout B"
    assert workout_dict["Workout B"].started_at == created_workouts[1].started_at
