# Tema: ubicación configurable del archivo SQLite persistente.

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, make_url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    db_url: str = Field(default="sqlite:///./data/portfolio.db", alias="DB_URL")

    @property
    def sqlalchemy_url(self) -> URL:
        url = make_url(self.db_url)
        if url.drivername not in {"sqlite", "sqlite+pysqlite"}:
            raise ValueError("DB_URL must use SQLite with the synchronous pysqlite driver.")
        if not url.database or url.database == ":memory:" or url.query:
            raise ValueError("SQLite persistence requires a file path without URI parameters.")
        if (
            url.username is not None
            or url.password is not None
            or url.host is not None
            or url.port is not None
        ):
            raise ValueError("SQLite URLs cannot contain credentials or a server address.")
        return url.set(drivername="sqlite+pysqlite")
