import pytest
import string
import random

from datetime import datetime

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.database import Base, get_db
from app import schemas


SKELETON_NAME_LENGTH = 25
random.seed(1234)


@pytest.fixture(scope="function")
def db_fixture():
    """Responsible for generating a session for the test database.

    Yields:
        Session: Test Database Session.
    """
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False}, poolclass=StaticPool)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(engine)
    session = Session(autocommit=False, autoflush=False, bind=engine)
    yield session
    Base.metadata.drop_all(bind=engine)
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def client(db_fixture: Session) -> TestClient:
    """Responsible for creating a client to the test database.

    Args:
        db_fixture (Session): Generated session for test database.

    Returns:
        TestClient: FastApi Test Client Object.
    """

    def _get_db_override():
        return db_fixture

    app = create_app()
    app.dependency_overrides[get_db] = _get_db_override
    return TestClient(app)


@pytest.fixture(scope="function")
def generate_users(client: TestClient) -> list[schemas.UserReply]:
    to_return = []

    for _ in range(10):
        name = "".join(random.choices(string.ascii_uppercase, k=SKELETON_NAME_LENGTH))
        height = round(random.uniform(1, 100), 4)
        weight = round(random.uniform(1, 300), 4)
        response = client.post("/User", json={"name": name, "height": height, "weight": weight})
        assert response.status_code == 200
        user = schemas.UserReply(**response.json())
        assert user.name == name
        assert user.height == height
        assert user.weight == weight
        to_return.append(user)
    return to_return


@pytest.fixture(scope="function")
def generate_exercises(client: TestClient) -> list[schemas.Exercise]:
    to_return = []

    for _ in range(10):
        exercise_name = "".join(random.choices(string.ascii_uppercase, k=SKELETON_NAME_LENGTH))
        exercise_description = "".join(random.choices(string.ascii_uppercase, k=SKELETON_NAME_LENGTH * 2))
        response = client.post("/Exercise", json={"name": exercise_name, "description": exercise_description})
        assert response.status_code == 200
        exercise = schemas.Exercise(**response.json())
        assert exercise.name == exercise_name
        assert exercise.description == exercise_description
        to_return.append(exercise)

    return to_return


@pytest.fixture(scope="function")
def generate_workouts(client: TestClient, generate_users: list[schemas.UserReply]) -> list[schemas.WorkoutReply]:
    to_return = []

    for user in generate_users:
        workout_name = "".join(random.choices(string.ascii_uppercase, k=SKELETON_NAME_LENGTH))
        started_at = datetime.now()
        response = client.post("/Workout", json={"name": workout_name, "user_id": user.id, "started_at": started_at.isoformat()})
        assert response.status_code == 200
        workout = schemas.WorkoutReply(**response.json())
        assert workout.name == workout_name
        assert workout.started_at is not None
        to_return.append(workout)

    return to_return


@pytest.fixture(scope="function")
def generate_sets(
    client: TestClient,
    generate_users: list[schemas.UserReply],
    generate_workouts: list[schemas.WorkoutReply],
    generate_exercises: list[schemas.Exercise],
) -> list[schemas.SetReply]:
    to_return = []

    for _ in range(10):
        random_workout = random.choice(generate_workouts)
        random_exercise = random.choice(generate_exercises)
        random_user = random.choice(generate_users)

        reps = random.randint(1, 10)
        weight = round(random.uniform(0, 100), 2)
        duration = random.randint(0, 300)
        date = datetime.now().date().isoformat()
        exercise_id = random_exercise.id
        workout_id = random_workout.id
        user_id = random_user.id

        response = client.post(
            "/Set",
            json={
                "reps": reps,
                "weight": weight,
                "duration": duration,
                "date": date,
                "exercise_id": exercise_id,
                "workout_id": workout_id,
                "user_id": user_id,
            },
        )
        assert response.status_code == 200
        created_set = schemas.SetReply(**response.json())
        assert created_set.reps == reps
        assert created_set.weight == weight
        assert created_set.duration == duration
        assert created_set.date.isoformat() == date
        assert created_set.exercise.id == exercise_id
        assert created_set.workout.id == workout_id
        assert created_set.user.id == user_id
        to_return.append(created_set)

    return to_return


@pytest.fixture(scope="function")
def generate_user_metrics(client: TestClient, generate_users: list[schemas.UserReply]) -> list[schemas.UserMetricsReply]:
    to_return = []

    for user in generate_users:
        # Create multiple metrics per user
        for _ in range(3):
            metrics_data = {"user_id": user.id, "weight": round(random.uniform(100, 250), 2), "height": round(random.uniform(60, 80), 2)}

            # Create metrics using the user metrics endpoint
            response = client.post(f"/User/{user.id}/metrics", json=metrics_data)
            assert response.status_code == 200
            metrics = schemas.UserMetricsReply(**response.json())
            to_return.append(metrics)

    return to_return
