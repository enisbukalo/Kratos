import string
import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from app import schemas

STRING_LENGTH = 15


def test_create_user(client: TestClient, generate_users: list[schemas.UserReply]):
    pass


def test_get_users(client: TestClient, generate_users: list[schemas.UserReply], generate_user_metrics: list[schemas.UserMetricsReply]):
    ids = [i.id for i in generate_users]

    for id in ids:
        response = client.get(f"/User/{id}")
        assert response.status_code == 200
        user = schemas.UserReply(**response.json())

        # Check user metrics
        assert len(user.metrics) > 0
        for metric in user.metrics:
            assert metric.user_id == user.id
            assert isinstance(metric.weight, float)
            assert isinstance(metric.height, float)
            assert isinstance(metric.recorded_at, datetime)

    response = client.get(f"/User?page_size=100&page_number=1")
    for user_data in response.json():
        user = schemas.UserReply(**user_data)
        assert len(user.metrics) > 0


def test_delete_users(client: TestClient, generate_users: list[schemas.UserReply], generate_user_metrics: list[schemas.UserMetricsReply]):
    for user in generate_users:
        # Get metrics before deletion
        response = client.get(f"/User/{user.id}")
        assert response.status_code == 200
        user_data = schemas.UserReply(**response.json())
        metrics_ids = [m.id for m in user_data.metrics]

        # Delete user
        response = client.delete(f"/User/{user.id}")
        assert response.status_code == 200

        # Verify user is deleted
        response = client.get(f"/User/{user.id}")
        assert response.status_code == 404

        # Verify metrics are cascade deleted
        for metric_id in metrics_ids:
            response = client.get(f"/UserMetrics/{metric_id}")
            assert response.status_code == 404

    response = client.get(f"/User?page_size=100&page_number=1")
    assert len(response.json()) == 0


def test_update_users(client: TestClient, generate_users: list[schemas.UserReply]):
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


def test_user_metrics_history(client: TestClient, generate_users: list[schemas.UserReply], generate_user_metrics: list[schemas.UserMetricsReply]):
    for user in generate_users:
        response = client.get(f"/User/{user.id}")
        assert response.status_code == 200
        user_data = schemas.UserReply(**response.json())

        # Verify metrics are ordered by recorded_at
        metrics = user_data.metrics
        for i in range(1, len(metrics)):
            assert metrics[i].recorded_at >= metrics[i - 1].recorded_at
