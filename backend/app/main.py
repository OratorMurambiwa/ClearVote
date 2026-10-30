"""Main FastAPI application for the ClearVote backend."""

from fastapi import FastAPI

from backend.app.config.ApplicationConfig import ApplicationConfig


app = FastAPI(
    title=ApplicationConfig.APP_NAME,
    version=ApplicationConfig.APP_VERSION,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health response for local and deployed checks."""
    return {
        "status": "ok",
        "environment": ApplicationConfig.get_environment(),
    }