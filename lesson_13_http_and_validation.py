# Tema: consumo de APIs, códigos HTTP, timeouts y validación con Pydantic.

import argparse
from decimal import ROUND_HALF_UP, Decimal

import httpx
from pydantic import ValidationError

from expense_tracker.rates import fetch_rates


def mock_response(request: httpx.Request) -> httpx.Response:
    # El transporte simula respuestas HTTP distintas según la ruta solicitada.
    if request.url.path == "/invalid":
        return httpx.Response(200, json={"base": "USD", "rates": {"EUR": "-1"}})
    if request.url.path == "/unavailable":
        return httpx.Response(503, json={"error": "Service unavailable"})
    return httpx.Response(200, json={"base": "USD", "rates": {"EUR": "0.92"}})


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate an exchange-rate API response.")
    parser.add_argument("--url", help="Optional live endpoint matching the documented contract")
    args = parser.parse_args()
    # Solo se consulta la red si el usuario proporciona --url con un endpoint real.
    # El contrato esperado es {"base": "USD", "rates": {"EUR": "0.92"}}.
    transport = None if args.url else httpx.MockTransport(mock_response)
    urls = (
        [args.url]
        if args.url
        else [
            "https://rates.example.test/latest",
            "https://rates.example.test/invalid",
            "https://rates.example.test/unavailable",
        ]
    )
    with httpx.Client(transport=transport, timeout=5.0) as client:
        # El contexto cierra el cliente; timeout limita la espera de las operaciones de red.
        for url in urls:
            try:
                quote = fetch_rates(client, url)
                # fetch_rates verifica el estado HTTP y valida el contenido con Pydantic.
                print("Validated quote:", quote.model_dump())
                if quote.base == "USD" and "EUR" in quote.rates:
                    converted = (Decimal("12.50") * quote.rates["EUR"]).quantize(
                        Decimal("0.01"), rounding=ROUND_HALF_UP
                    )
                    print("Converted sample amount in EUR:", converted)
            except httpx.HTTPStatusError as error:
                # Una respuesta de error, un fallo de conexión y datos inválidos son casos diferentes.
                print("HTTP error:", error.response.status_code)
            except httpx.RequestError as error:
                print("Network error:", error)
            except ValidationError as error:
                print("Invalid response:", error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
