import string
import random

from datetime import datetime, timedelta

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
