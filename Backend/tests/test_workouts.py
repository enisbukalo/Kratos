import string
import random

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_workout(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    pass


def test_get_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    ids = [i.id for i in generate_workouts]

    for id in ids:
        response = client.get(f"/Workout/{id}")
        assert response.status_code == 200
        assert schemas.WorkoutReply(**response.json()) in generate_workouts

    response = client.get(f"/Workout?page_size=100&page_number=1")
    for workout in response.json():
        assert schemas.WorkoutReply(**workout) in generate_workouts


def test_delete_workouts(client: TestClient, generate_workouts: list[schemas.WorkoutReply]):
    for workout in generate_workouts:
        response = client.delete(f"/Workout/{workout.id}")
        assert response.status_code == 200

        response = client.get(f"/Workout/{workout.id}")
        assert response.status_code == 404

    response = client.get(f"/Workout?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_workouts(client: TestClient, generate_users: list[schemas.User], generate_workouts: list[schemas.WorkoutReply]):
    for workout in generate_workouts:
        new_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))
        new_user = random.choice(generate_users)
        response = client.put(f"/Workout/{workout.id}", json={"name": new_name, "user_id": new_user.id})
        assert response.status_code == 200

        new_workout = schemas.Workout(**response.json())
        assert new_workout.name == new_name
