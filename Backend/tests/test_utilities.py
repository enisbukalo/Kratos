from fastapi.testclient import TestClient


def test_reset_database(client: TestClient, generate_sets: list):
    # First verify we have data
    response = client.get("/User?page_size=100&page_number=1&sort=false")
    assert len(response.json()) > 0

    # Reset database
    response = client.post("/Utility/reset-database")
    assert response.status_code == 200
    assert response.json()["message"] == "Database reset successfully"
