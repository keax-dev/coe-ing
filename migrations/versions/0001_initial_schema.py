# Tema: esquema inicial explícito de instituciones y educación para bases nuevas.

import sqlalchemy as sa
from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Esta revisión solo se aplica a una base nueva; una existente requiere verificar y registrar la línea base.
    op.create_table(
        "institution",
        sa.Column(
            "institution_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            sa.Identity(),
            primary_key=True,
        ),
        sa.Column("institution_name", sa.String(255), nullable=False),
        sa.Column("institution_name_es", sa.String(255)),
        sa.Column("institution_url", sa.String(2048)),
        sa.Column("institution_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("version", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
    )
    op.create_table(
        "education",
        sa.Column(
            "education_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            sa.Identity(),
            primary_key=True,
        ),
        sa.Column("education_title", sa.String(255), nullable=False),
        sa.Column("education_title_es", sa.String(255)),
        sa.Column("education_place", sa.String(255), nullable=False),
        sa.Column("education_start", sa.String(255)),
        sa.Column("education_start_es", sa.String(255)),
        sa.Column("education_end", sa.String(255), nullable=False),
        sa.Column("education_end_es", sa.String(255)),
        sa.Column("education_position", sa.Integer(), nullable=False),
        sa.Column("education_deleted", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("education_visible", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "institution_id",
            sa.BigInteger(),
            sa.ForeignKey("institution.institution_id"),
            nullable=False,
        ),
        sa.Column("version", sa.BigInteger(), server_default=sa.text("0"), nullable=False),
    )


def downgrade() -> None:
    # La reversión elimina estas tablas; nunca se ejecuta al arrancar la API.
    op.drop_table("education")
    op.drop_table("institution")
