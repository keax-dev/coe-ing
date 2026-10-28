# Simulamos HTTP y validamos datos externos sin realizar llamadas de red.

import asyncio
from decimal import Decimal

import httpx
import pytest
from pydantic import ValidationError

from expense_tracker.rates import ExchangeRates, fetch_rates, fetch_rates_async


def test_valid_http_response() -> None:
    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json={"base": "USD", "rates": {"EUR": "0.92"}})
    )
    with httpx.Client(transport=transport) as client:
        assert fetch_rates(client, "https://rates.example.test/latest").rates["EUR"] == Decimal(
            "0.92"
        )


@pytest.mark.parametrize("rate", ["-1", "0", "NaN", "Infinity", "text"])
def test_invalid_rates(rate: str) -> None:
    with pytest.raises(ValidationError):
        ExchangeRates.model_validate({"base": "USD", "rates": {"EUR": rate}})


@pytest.mark.parametrize(
    "payload",
    [
        {"base": "usd", "rates": {"EUR": "1"}},
        {"base": "USD", "rates": {}},
        {"base": "USD", "rates": {"euro": "1"}},
    ],
)
def test_invalid_response_contract(payload: dict[str, object]) -> None:
    with pytest.raises(ValidationError):
        ExchangeRates.model_validate(payload)


def test_http_error_is_not_treated_as_success() -> None:
    with httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(503))) as client:
        with pytest.raises(httpx.HTTPStatusError):
            fetch_rates(client, "https://rates.example.test/latest")


def test_network_timeout_is_propagated() -> None:
    def timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Timed out", request=request)

    with httpx.Client(transport=httpx.MockTransport(timeout)) as client:
        with pytest.raises(httpx.ReadTimeout):
            fetch_rates(client, "https://rates.example.test/latest")


def test_async_http_response() -> None:
    async def check() -> None:
        transport = httpx.MockTransport(
            lambda request: httpx.Response(200, json={"base": "USD", "rates": {"EUR": "0.92"}})
        )
        async with httpx.AsyncClient(transport=transport) as client:
            quote = await fetch_rates_async(client, "https://rates.example.test/latest")
            assert quote.base == "USD"

    asyncio.run(check())
