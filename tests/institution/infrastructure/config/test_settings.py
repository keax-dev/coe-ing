# Tema: adaptación de configuración JDBC y protección de credenciales.

from src.institution.infrastructure.config.settings import Settings


def test_jdbc_conversion_preserves_special_password_characters() -> None:
    settings = Settings(
        _env_file=None,
        DB_URL="jdbc:postgresql://localhost:5432/portfolio_db",
        DB_USERNAME="postgres",
        DB_PASSWORD="p@ss:/word",
        DB_DRIVER="org.postgresql.Driver",
    )
    assert settings.sqlalchemy_url.drivername == "postgresql+psycopg"
    assert settings.sqlalchemy_url.password == "p@ss:/word"
    assert "p@ss:/word" not in repr(settings)
