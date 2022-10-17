import uvicorn

from moderation_service.app import app


def start() -> None:
    """Starts the FastAPI server."""
    uvicorn.run(app, host="0.0.0.0", port=8000)
