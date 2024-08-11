import string
import random

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_skeletons(client: TestClient, generate_skeletons: list[schemas.Skeleton]):
    pass


def test_get_skeletons(client: TestClient, generate_skeletons: list[schemas.Skeleton]):
    response = client.get(f"Skeleton?page_size=100&page_number=1")
    assert response.status_code == 200
    assert len(response.json()) == 100
    retrieved_skeletons = [schemas.Skeleton(**skeleton) for skeleton in response.json()]

    for retrieved_skeleton in retrieved_skeletons:
        assert retrieved_skeleton in generate_skeletons


def test_delete_skeleton(client: TestClient, generate_skeletons: list[schemas.Skeleton]):
    for i in range(len(generate_skeletons)):
        response = client.delete(f"Skeleton/{generate_skeletons[i].id}")
        assert response.status_code == 200

        response = client.get(f"Skeleton/{generate_skeletons[i].id}")
        assert response.status_code == 404


def test_update_skeleton(client: TestClient, generate_skeletons: list[schemas.Skeleton]):
    for _ in range(len(generate_skeletons)):
        random_skeleton = random.choice(generate_skeletons)
        updated_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=50))
        updated_height = round(random.uniform(0.0, 3.0), 4)

        response = client.put(f"Skeleton/{random_skeleton.id}", json={"name": updated_name, "height_m": updated_height})
        assert response.status_code == 200
        updated_skeleton = schemas.Skeleton(**response.json())
        assert updated_skeleton.id == random_skeleton.id
        assert updated_skeleton.name == updated_name
        assert updated_skeleton.height_m == updated_height

        response = client.get(f"Skeleton/{random_skeleton.id}")
        assert response.status_code == 200
        retrieved_skeleton = schemas.Skeleton(**response.json())
        assert retrieved_skeleton == updated_skeleton
