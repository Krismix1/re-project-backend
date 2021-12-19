"""Module for application configuration."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Config class."""

    class Config:
        """Configuration for pydantic."""

        # The .env file can be used to overwrite any default env vars for local development.
        # The file is gitignored, so feel free to create it on your machine if you need it.
        env_file = ".env"
        case_sensitive = True


SETTINGS = Settings()
