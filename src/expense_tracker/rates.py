# Tema: validación de tasas y clientes HTTP inyectables.

import re
from decimal import Decimal

import httpx
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ExchangeRates(BaseModel):
    # Rechazamos campos extra para detectar respuestas que cambien el contrato esperado.
    model_config = ConfigDict(extra="forbid")

    base: str = Field(pattern=r"^[A-Z]{3}$")
    rates: dict[str, Decimal]

    @field_validator("rates")
    @classmethod
    def validate_rates(cls, values: dict[str, Decimal]) -> dict[str, Decimal]:
        # El tipado convierte valores a Decimal; este validador añade reglas del dominio.
        if not values:
            raise ValueError("At least one exchange rate is required.")
        for currency, rate in values.items():
            if not re.fullmatch(r"[A-Z]{3}", currency):
                raise ValueError("Currency codes must contain three uppercase letters.")
            if not rate.is_finite() or rate <= 0:
                raise ValueError("Exchange rates must be finite and positive.")
        return values


def fetch_rates(client: httpx.Client, url: str) -> ExchangeRates:
    # Inyectar el cliente permite usar un transporte real o uno simulado sin cambiar esta función.
    response = client.get(url)
    # No intentamos interpretar como éxito una respuesta HTTP de error.
    response.raise_for_status()
    return ExchangeRates.model_validate_json(response.content)


async def fetch_rates_async(client: httpx.AsyncClient, url: str) -> ExchangeRates:
    # await cede el control mientras el cliente espera la respuesta.
    response = await client.get(url)
    response.raise_for_status()
    return ExchangeRates.model_validate_json(response.content)
