import random

from datetime import datetime, timedelta, date

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_set(client: TestClient, generate_sets: list[schemas.SetReply]):
    pass


def test_get_sets(client: TestClient, generate_sets: list[schemas.SetReply]):
    ids = [i.id for i in generate_sets]

    for id in ids:
        response = client.get(f"/Set/{id}")
        assert response.status_code == 200
        assert schemas.SetReply(**response.json()) in generate_sets

    response = client.get(f"/Set?page_size=100&page_number=1")
    for set in response.json():
        assert schemas.SetReply(**set) in generate_sets


def test_delete_sets(client: TestClient, generate_sets: list[schemas.SetReply]):
    for set in generate_sets:
        response = client.delete(f"/Set/{set.id}")
        assert response.status_code == 200

        response = client.get(f"/Set/{set.id}")
        assert response.status_code == 404

    response = client.get(f"/Set?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_sets(client: TestClient, generate_sets: list[schemas.SetReply]):
    for set in generate_sets:
        new_reps = random.randint(1, 100)
        new_weight = round(random.uniform(0, 100), 2)
        new_duration = random.randint(0, 300)
        new_distance = round(random.uniform(0, 1000), 2)
        new_date = (datetime.now() + timedelta(days=random.randint(-5, 5))).date().isoformat()

        response = client.put(
            f"/Set/{set.id}",
            json={
                "reps": new_reps,
                "weight": new_weight,
                "duration": new_duration,
                "distance": new_distance,
                "date": new_date,
                "exercise_id": set.exercise.id,
                "workout_id": set.workout.id,
                "user_id": set.user.id,
            },
        )
        assert response.status_code == 200

        new_set = schemas.ExerciseSet(**response.json())
        assert new_set.id == set.id
        assert new_set.reps == new_reps
        assert new_set.weight == new_weight
        assert new_set.duration == new_duration
        assert new_set.distance == new_distance
        assert new_set.date.isoformat() == new_date


def test_create_sets_success(client, generate_exercises, generate_workouts, generate_users):
    # Get random test data from fixtures
    exercise = random.choice(generate_exercises)
    workout = random.choice(generate_workouts)
    user = random.choice(generate_users)

    sets_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [
            {"reps": 5, "weight": 100.0, "duration": 0, "distance": 0.0, "date": str(date.today())},
            {"reps": 5, "weight": 102.5, "duration": 0, "distance": 0.0, "date": str(date.today())},
        ],
    }

    response = client.post("/Set/bulk", json=sets_data)
    assert response.status_code == 200

    created_sets = response.json()
    assert len(created_sets) == 2

    # Verify first set
    assert created_sets[0]["reps"] == 5
    assert created_sets[0]["weight"] == 100.0
    assert created_sets[0]["exercise"]["id"] == exercise.id
    assert created_sets[0]["workout"]["id"] == workout.id
    assert created_sets[0]["user"]["id"] == user.id

    # Verify second set
    assert created_sets[1]["reps"] == 5
    assert created_sets[1]["weight"] == 102.5
    assert created_sets[1]["exercise"]["id"] == exercise.id
    assert created_sets[1]["workout"]["id"] == workout.id
    assert created_sets[1]["user"]["id"] == user.id


def test_create_sets_invalid_exercise(client, generate_workouts, generate_users):
    workout = random.choice(generate_workouts)
    user = random.choice(generate_users)

    sets_data = {
        "exercise_id": 99999,  # Non-existent exercise ID
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [{"reps": 5, "weight": 100.0, "duration": 0, "distance": 0.0, "date": str(date.today())}],
    }

    response = client.post("/Set/bulk", json=sets_data)
    assert response.status_code == 404
    assert "No Exercise With Id" in response.json()["detail"]


def test_create_sets_invalid_workout(client, generate_exercises, generate_users):
    exercise = random.choice(generate_exercises)
    user = random.choice(generate_users)

    sets_data = {
        "exercise_id": exercise.id,
        "workout_id": 99999,  # Non-existent workout ID
        "user_id": user.id,
        "sets": [{"reps": 5, "weight": 100.0, "duration": 0, "distance": 0.0, "date": str(date.today())}],
    }

    response = client.post("/Set/bulk", json=sets_data)
    assert response.status_code == 404
    assert "No Workout With Id" in response.json()["detail"]


def test_create_sets_invalid_user(client, generate_exercises, generate_workouts):
    exercise = random.choice(generate_exercises)
    workout = random.choice(generate_workouts)

    sets_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": 99999,  # Non-existent user ID
        "sets": [{"reps": 5, "weight": 100.0, "duration": 0, "distance": 0.0, "date": str(date.today())}],
    }

    response = client.post("/Set/bulk", json=sets_data)
    assert response.status_code == 404
    assert "No User With Id" in response.json()["detail"]


def test_create_sets_empty_sets_list(client, generate_exercises, generate_workouts, generate_users):
    exercise = random.choice(generate_exercises)
    workout = random.choice(generate_workouts)
    user = random.choice(generate_users)

    sets_data = {"exercise_id": exercise.id, "workout_id": workout.id, "user_id": user.id, "sets": []}

    response = client.post("/Set/bulk", json=sets_data)
    assert response.status_code == 200
    assert response.json() == []


def test_bulk_update_sets(client, generate_users, generate_workouts, generate_exercises):
    # Get random test data
    exercise = random.choice(generate_exercises)
    workout = random.choice(generate_workouts)
    user = random.choice(generate_users)

    # First create some sets
    create_sets_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [
            {"reps": 5, "weight": 100.0, "duration": 0, "distance": 0.0, "date": str(date.today())},
            {"reps": 5, "weight": 102.5, "duration": 0, "distance": 0.0, "date": str(date.today())},
        ],
    }

    response = client.post("/Set/bulk", json=create_sets_data)
    assert response.status_code == 200
    created_sets = [schemas.SetReply(**s) for s in response.json()]
    assert len(created_sets) == 2

    # Now prepare update data for these sets
    update_sets_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [
            {"id": created_sets[0].id, "reps": 8, "weight": 110.0, "duration": 60, "distance": 0.0, "date": str(date.today())},
            {"id": created_sets[1].id, "reps": 10, "weight": 115.0, "duration": 45, "distance": 0.0, "date": str(date.today())},
        ],
    }

    # Update the sets
    response = client.put("/Set/bulk", json=update_sets_data)
    assert response.status_code == 200
    updated_sets = response.json()
    assert len(updated_sets) == 2

    # Verify first set
    assert updated_sets[0]["reps"] == 8
    assert updated_sets[0]["weight"] == 110.0
    assert updated_sets[0]["duration"] == 60
    assert updated_sets[0]["exercise"]["id"] == exercise.id
    assert updated_sets[0]["workout"]["id"] == workout.id
    assert updated_sets[0]["user"]["id"] == user.id

    # Verify second set
    assert updated_sets[1]["reps"] == 10
    assert updated_sets[1]["weight"] == 115.0
    assert updated_sets[1]["duration"] == 45
    assert updated_sets[1]["exercise"]["id"] == exercise.id
    assert updated_sets[1]["workout"]["id"] == workout.id
    assert updated_sets[1]["user"]["id"] == user.id


def test_delete_empty_sets(client: TestClient, generate_sets: list[schemas.SetReply]):
    # Create some empty sets
    exercise = generate_sets[0].exercise
    workout = generate_sets[0].workout
    user = generate_sets[0].user

    empty_sets_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [
            {"reps": 0, "weight": 0, "duration": 0, "distance": 0, "date": str(date.today())},
            {"reps": 0, "weight": 0, "duration": 0, "distance": 0, "date": str(date.today())},
        ],
    }

    # Create non-empty set
    non_empty_set_data = {
        "exercise_id": exercise.id,
        "workout_id": workout.id,
        "user_id": user.id,
        "sets": [
            {"reps": 5, "weight": 100, "duration": 60, "distance": 0, "date": str(date.today())},
        ],
    }

    # Add the sets to the database
    response = client.post("/Set/bulk", json=empty_sets_data)
    assert response.status_code == 200
    empty_sets = response.json()
    assert len(empty_sets) == 2

    response = client.post("/Set/bulk", json=non_empty_set_data)
    assert response.status_code == 200
    non_empty_sets = response.json()
    assert len(non_empty_sets) == 1

    # Delete empty sets
    response = client.delete("/Set/empty")
    assert response.status_code == 200
    result = response.json()
    assert result["deleted_count"] == 2
    assert "Successfully deleted 2 empty sets" in result["message"]

    # Verify empty sets were deleted but non-empty set remains
    response = client.get(f"/Set?page_size=100&page_number=1")
    remaining_sets = response.json()

    # Should only have the non-empty set and any sets from generate_sets
    assert len(remaining_sets) == len(generate_sets) + 1

    # Verify the remaining set has non-zero values
    for set in remaining_sets:
        assert not (set["reps"] == 0 and set["weight"] == 0 and set["duration"] == 0 and set["distance"] == 0)
