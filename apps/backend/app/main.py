from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.agent import router as agent_router
from app.api.routes.health import router as health_router
from app.api.routes.stories import router as stories_router


def create_app() -> FastAPI:
    app = FastAPI(title="shared-story")
    register_exception_handlers(app)
    app.include_router(health_router, prefix="/api/v1")
    app.include_router(stories_router, prefix="/api/v1")
    app.include_router(agent_router, prefix="/api/v1")
    return app


app = create_app()
