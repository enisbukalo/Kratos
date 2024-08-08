import string
import random

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_bones(client: TestClient, generate_bones: list[schemas.Bone]):
    pass


def test_get_bones(client: TestClient, generate_bones: list[schemas.Bone]):
    response = client.get(f"Bone?page_size=100&page_number=1")
    assert response.status_code == 200
    assert len(response.json()) == 100
    retrieved_bones = [schemas.Bone(**bone) for bone in response.json()]

    for retrieved_bone in retrieved_bones:
        assert retrieved_bone in generate_bones


def test_delete_bone(client: TestClient, generate_bones: list[schemas.Bone]):
    for i in range(len(generate_bones)):
        response = client.delete(f"Bone/{generate_bones[i].id}")
        assert response.status_code == 200

        response = client.get(f"Bone/{generate_bones[i].id}")
        assert response.status_code == 404


def test_update_bone(client: TestClient, generate_bones: list[schemas.Bone]):
    for _ in range(len(generate_bones)):
        random_bone = random.choice(generate_bones)
        updated_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=50))
        updated_height = round(random.uniform(200.0, 400.0), 4)

        response = client.put(f"Bone/{random_bone.id}", json={"name": updated_name, "height_m": updated_height})
        assert response.status_code == 200
        updated_bone = schemas.Bone(**response.json())
        assert updated_bone.id == random_bone.id
        assert updated_bone.name == updated_name
        assert updated_bone.length_cm == updated_height

        response = client.get(f"Bone/{random_bone.id}")
        assert response.status_code == 200
        retrieved_bone = schemas.Bone(**response.json())
        assert retrieved_bone == updated_bone
