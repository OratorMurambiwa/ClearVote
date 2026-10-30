"""Application configuration for the ClearVote backend."""

import os


class ApplicationConfig:
    """Provides backend configuration from environment variables."""

    APP_NAME = "ClearVote API"
    APP_VERSION = "0.1.0"

    @staticmethod
    def get_environment() -> str:
        """Return the current application environment."""
        return os.getenv("CLEARVOTE_ENV", "development")

    @staticmethod
    def get_allowed_origin() -> str:
        """Return the frontend origin allowed to access the API."""
        return os.getenv("CLEARVOTE_ALLOWED_ORIGIN", "*")