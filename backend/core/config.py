"""Module for application configuration."""
from pydantic import BaseSettings, validator

# pylint:disable=no-self-use,no-self-argument,missing-function-docstring


class Settings(BaseSettings):
    """Config class."""

    DATABASE_URL: str = "postgresql://postgres:password@localhost/postgres"

    @validator("DATABASE_URL")
    def set_database_url(cls, value: str) -> str:
        # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
        # SQLAlchemy 1.4.x removed support for "postgres" and requires "postgresql"
        # however, Heroku uses "postgres", so this compatibility hack is needed
        if value.startswith("postgres://"):
            value = value.replace("postgres://", "postgresql://", 1)
        return value

    class Config:
        """Configuration for pydantic."""

        # The .env file can be used to overwrite any default env vars for local development.
        # The file is gitignored, so feel free to create it on your machine if you need it.
        env_file = ".env"
        case_sensitive = True


SETTINGS = Settings()
