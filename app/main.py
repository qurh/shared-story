from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.stories import router as stories_router


def create_app() -> FastAPI:
    app = FastAPI(title="shared-story")
    app.include_router(health_router, prefix="/api")
    app.include_router(stories_router, prefix="/api")
    return app


app = create_app()
