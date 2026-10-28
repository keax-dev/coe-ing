# Tema: variables de entorno y adaptación de la URL JDBC a psycopg.

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    db_url: str = Field(alias="DB_URL")
    db_username: str = Field(alias="DB_USERNAME")
    db_password: SecretStr = Field(alias="DB_PASSWORD")
    db_driver: str = Field(default="org.postgresql.Driver", alias="DB_DRIVER")

    @property
    def sqlalchemy_url(self) -> URL:
        url = make_url(self.db_url.removeprefix("jdbc:"))
        if url.get_backend_name() != "postgresql":
            raise ValueError("DB_URL must reference a PostgreSQL database.")
        if self.db_driver not in {"org.postgresql.Driver", "psycopg"}:
            raise ValueError("DB_DRIVER must be org.postgresql.Driver or psycopg.")
        # URL.set codifica contraseñas con caracteres especiales sin concatenarlas al texto.
        return url.set(
            drivername="postgresql+psycopg",
            username=self.db_username,
            password=self.db_password.get_secret_value(),
        )
