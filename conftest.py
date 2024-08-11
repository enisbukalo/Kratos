import pytest
import string
import random

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.main import create_app
from app.database import Base, get_db
from app import schemas


SKELETON_NAME_LENGTH = 25


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
def generate_skeletons(client: TestClient) -> list[schemas.Skeleton]:
    """Responsible for generating a list of Skeleton objects.

    Args:
        client (TestClient): FastApi Test Client.

    Returns:
        list[schemas.Skeleton]: Collection of Skeleton objects that were generated.
    """
    made_skeletons: list[schemas.Skeleton] = []

    for _ in range(100):
        skeleton_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=SKELETON_NAME_LENGTH))
        skeleton_height = round(random.uniform(0.0, 3.0), 4)

        response = client.post("Skeleton", json={"name": skeleton_name, "height_m": skeleton_height})
        assert response.status_code == 200

        skeleton = schemas.Skeleton(**response.json())
        assert skeleton.name == skeleton_name
        assert skeleton.height_m == skeleton_height
        made_skeletons.append(skeleton)

        response = client.get(f"Skeleton/{skeleton.id}")
        assert response.status_code == 200
        assert schemas.Skeleton(**response.json()) == skeleton

    return made_skeletons


@pytest.fixture(scope="function")
def generate_bones(client: TestClient, generate_skeletons: list[schemas.Skeleton]) -> list[schemas.Bone]:
    """Responsible for generating a list of Bone objects.

    Args:
        client (TestClient): FastApi Test Client.

    Returns:
        list[schemas.Bone]: Collection of Bone objects that were generated.
    """
    made_bones: list[schemas.Bone] = []

    for _ in range(100):
        bone_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=SKELETON_NAME_LENGTH))
        bone_length = round(random.uniform(10.0, 60.0), 4)
        random_skeleton = random.choice(generate_skeletons)

        response = client.post("Bone", json={"name": bone_name, "length_cm": bone_length, "skeleton_id": random_skeleton.id})
        assert response.status_code == 200

        bone = schemas.Bone(**response.json())
        assert bone.name == bone_name
        assert bone.length_cm == bone_length
        assert bone.skeleton_id == random_skeleton.id
        assert bone.skeleton == random_skeleton
        made_bones.append(bone)

    return made_bones
