# Tema: clientes HTTP, respuestas simuladas y validación externa con Pydantic.

from decimal import Decimal

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError


class ProductResponse(BaseModel):
    # Rechazamos campos inesperados y validamos restricciones además de convertir tipos.
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1)
    price: Decimal = Field(gt=0, allow_inf_nan=False)
    stock: int = Field(ge=0)


def simulate_response(request: httpx.Request) -> httpx.Response:
    # MockTransport sustituye la red; se mantiene el flujo real de solicitud y respuesta.
    if request.url.path == "/invalid":
        return httpx.Response(200, json={"name": "Book", "price": "-1", "stock": 3})
    if request.url.path == "/unavailable":
        return httpx.Response(503, json={"error": "Service unavailable"})
    if request.url.path == "/timeout":
        raise httpx.ReadTimeout("Simulated timeout", request=request)
    return httpx.Response(200, json={"name": "Book", "price": "12.50", "stock": 3})


def main() -> None:
    transport = httpx.MockTransport(simulate_response)
    # timeout limita las esperas; el contexto libera el cliente sin necesitar una aplicación web.
    with httpx.Client(transport=transport, timeout=5.0) as client:
        for path in ["/valid", "/invalid", "/unavailable", "/timeout"]:
            print("Request path:", path)
            try:
                response = client.get(f"https://products.example.test{path}")
                # Un HTTP de error no debe interpretarse como una respuesta válida del dominio.
                response.raise_for_status()
                product = ProductResponse.model_validate_json(response.content)
                print("Validated product:", product.model_dump())
            except httpx.HTTPStatusError as error:
                print("HTTP error:", error.response.status_code)
            except httpx.RequestError as error:
                print("Network error:", error)
            except ValidationError as error:
                print("Invalid product:", error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
