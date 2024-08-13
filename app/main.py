from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from .routers import skeleton, bone
from .routers import exercises, sets, workouts, users


def create_app() -> FastAPI:
    origins = ["*"]

    created_app = FastAPI(title="Kratos FastAPI", version="0.0.1")

    created_app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

    created_app.include_router(skeleton.router)
    created_app.include_router(bone.router)

    created_app.include_router(users.router)
    created_app.include_router(workouts.router)
    created_app.include_router(sets.router)
    created_app.include_router(exercises.router)

    return created_app


app = create_app()
