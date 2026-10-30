# Tema: configuración mínima y validación del archivo SQLite persistente.

import pytest

from src.shared.config.settings import Settings


def test_only_database_url_is_required() -> None:
    settings = Settings(_env_file=None, DB_URL="sqlite:///./data/portfolio.db")
    assert settings.sqlalchemy_url.drivername == "sqlite+pysqlite"
    assert settings.sqlalchemy_url.database == "./data/portfolio.db"
    assert settings.sqlalchemy_url.username is None
    assert settings.sqlalchemy_url.password is None


def test_default_database_is_persistent_sqlite(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DB_URL", raising=False)
    assert Settings(_env_file=None).sqlalchemy_url.drivername == "sqlite+pysqlite"


@pytest.mark.parametrize(
    "url",
    [
        "mysql://localhost/db",
        "sqlite://",
        "sqlite:///:memory:",
        "sqlite+aiosqlite:///data.db",
        "sqlite:///file:db?mode=memory&uri=true",
        "sqlite://localhost/data.db",
    ],
)
def test_unsupported_or_nonpersistent_urls_are_rejected(url: str) -> None:
    with pytest.raises(ValueError):
        Settings(_env_file=None, DB_URL=url).sqlalchemy_url
