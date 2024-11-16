import string
import random

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_exercise(client: TestClient, generate_exercises: list[schemas.Exercise]):
    pass


def test_get_exercises(client: TestClient, generate_exercises: list[schemas.Exercise]):
    ids = [i.id for i in generate_exercises]

    for id in ids:
        response = client.get(f"/Exercise/{id}")
        assert response.status_code == 200
        assert schemas.Exercise(**response.json()) in generate_exercises

    response = client.get(f"/Exercise?page_size=100&page_number=1")
    for exercise in response.json():
        assert schemas.Exercise(**exercise) in generate_exercises


def test_delete_exercises(client: TestClient, generate_exercises: list[schemas.Exercise]):
    for exercise in generate_exercises:
        response = client.delete(f"/Exercise/{exercise.id}")
        assert response.status_code == 200

        response = client.get(f"/Exercise/{exercise.id}")
        assert response.status_code == 404

    response = client.get(f"/Exercise?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_exercises(client: TestClient, generate_exercises: list[schemas.Exercise]):
    for exercise in generate_exercises:
        new_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))
        new_description = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH * 2))
        response = client.put(f"/Exercise/{exercise.id}", json={"name": new_name, "description": new_description})
        assert response.status_code == 200

        new_exercise = schemas.Exercise(**response.json())
        assert new_exercise.name == new_name
        assert new_exercise.description == new_description
