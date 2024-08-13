import string
import random

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_user(client: TestClient, generate_users: list[schemas.User]):
    pass


def test_get_users(client: TestClient, generate_users: list[schemas.User]):
    ids = [i.id for i in generate_users]

    for id in ids:
        response = client.get(f"/User/{id}")
        assert response.status_code == 200
        assert schemas.UserReply(**response.json()) in generate_users

    response = client.get(f"/User?page_size=100&page_number=1")
    for user in response.json():
        assert schemas.UserReply(**user) in generate_users


def test_delete_users(client: TestClient, generate_users: list[schemas.User]):
    for user in generate_users:
        response = client.delete(f"/User/{user.id}")
        assert response.status_code == 200

        response = client.get(f"/User/{user.id}")
        assert response.status_code == 404

    response = client.get(f"/User?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_users(client: TestClient, generate_users: list[schemas.User]):
    for user in generate_users:
        new_name = "".join(random.choices(string.ascii_uppercase, k=STRING_LENGTH))
        new_height = round(random.uniform(1, 100), 4)
        new_weight = round(random.uniform(1, 300), 4)
        response = client.put(f"/User/{user.id}", json={"name": new_name, "height": new_height, "weight": new_weight})
        assert response.status_code == 200

        new_user = schemas.User(**response.json())
        assert new_user.name == new_name
        assert new_user.height == new_height
        assert new_user.weight == new_weight
