import pytest
from datetime import datetime
import random
from fastapi.testclient import TestClient
from app import schemas


def test_create_user_metrics(client: TestClient, generate_users: list[schemas.UserReply]):
    for user in generate_users:
        # Create metrics for user
        metrics_data = {"weight": round(random.uniform(100, 250), 2), "height": round(random.uniform(60, 80), 2)}

        response = client.post(f"/User/{user.id}/metrics", json=metrics_data)
        assert response.status_code == 200
        metrics = schemas.UserMetricsReply(**response.json())

        # Verify metrics data
        assert metrics.user_id == user.id
        assert metrics.weight == metrics_data["weight"]
        assert metrics.height == metrics_data["height"]
        assert metrics.recorded_at is not None


def test_get_user_metrics(client: TestClient, generate_users: list[schemas.UserReply]):
    # First create some metrics
    test_metrics = []
    for user in generate_users:
        metrics_data = {"weight": round(random.uniform(100, 250), 2), "height": round(random.uniform(60, 80), 2)}

        response = client.post(f"/User/{user.id}/metrics", json=metrics_data)
        assert response.status_code == 200
        test_metrics.append(schemas.UserMetricsReply(**response.json()))

    # Get metrics for each user
    for user in generate_users:
        response = client.get(f"/User/{user.id}/metrics")
        assert response.status_code == 200
        metrics_list = [schemas.UserMetricsReply(**m) for m in response.json()]

        # Verify metrics data
        assert len(metrics_list) > 0
        for metric in metrics_list:
            assert metric.user_id == user.id
            assert isinstance(metric.weight, float)
            assert isinstance(metric.height, float)
            assert isinstance(metric.recorded_at, datetime)


def test_user_metrics_history(client: TestClient, generate_users: list[schemas.UserReply]):
    # Create multiple metrics entries for a single user
    user = generate_users[0]
    test_metrics = []

    for _ in range(5):
        metrics_data = {"weight": round(random.uniform(100, 250), 2), "height": round(random.uniform(60, 80), 2)}

        response = client.post(f"/User/{user.id}/metrics", json=metrics_data)
        assert response.status_code == 200
        test_metrics.append(schemas.UserMetricsReply(**response.json()))

    # Get metrics and verify they're all present
    response = client.get(f"/User/{user.id}/metrics")
    assert response.status_code == 200
    metrics_list = [schemas.UserMetricsReply(**m) for m in response.json()]

    assert len(metrics_list) == 6


def test_invalid_user_metrics(client: TestClient):
    # Test creating metrics for non-existent user
    metrics_data = {"weight": 150.5, "height": 70.0}

    response = client.post("/User/99999/metrics", json=metrics_data)
    assert response.status_code == 404

    # Test creating metrics with invalid data
    invalid_metrics = [
        {"weight": -1, "height": 70.0},  # negative weight
        {"weight": 150.5, "height": -1},  # negative height
        {"weight": 0, "height": 70.0},  # zero weight
        {"weight": 150.5, "height": 0},  # zero height
    ]

    # Use a valid user ID from generate_users
    for invalid_data in invalid_metrics:
        response = client.post("/User/1/metrics", json=invalid_data)
        assert response.status_code == 422
