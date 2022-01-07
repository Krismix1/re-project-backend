"""Module for application configuration."""
from pydantic import BaseSettings, SecretStr, validator

# pylint:disable=no-self-use,no-self-argument


class Settings(BaseSettings):
    """Config class."""

    BUILD_ID: str = "local"
    DATABASE_URL: str = "postgresql://postgres:password@localhost/postgres"

    # to get a string like this run:
    # openssl rand -hex 32
    JWT_SECRET_KEY: SecretStr = SecretStr(
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

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
