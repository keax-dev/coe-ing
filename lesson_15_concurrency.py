# Tema: concurrencia de entrada/salida, tareas asíncronas y procesos para cálculo.

import argparse
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

import httpx

from expense_tracker.rates import fetch_rates_async
from expense_tracker.sample_data import sample_expenses
from expense_tracker.serialization import load_json, save_json
from expense_tracker.services import total_amount


def read_total(path: Path) -> Decimal:
    return total_amount(load_json(path))


def calculate_checksum(limit: int) -> int:
    # Función de nivel superior: Windows debe poder importarla al crear un proceso.
    return sum(number * number for number in range(limit))


async def mock_response(request: httpx.Request) -> httpx.Response:
    # Cedemos el control para observar la coordinación de tareas sin consultar la red.
    await asyncio.sleep(0)
    return httpx.Response(200, json={"base": "USD", "rates": {"EUR": "0.92"}})


async def query_multiple_sources() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(mock_response), timeout=5.0
    ) as client:
        # TaskGroup espera todas las tareas y cancela las restantes si una falla.
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(fetch_rates_async(client, f"https://rates.example.test/{source}"))
                for source in ["first", "second", "third"]
            ]
        for task in tasks:
            print("Async source result:", task.result().rates)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare concurrency mechanisms.")
    parser.add_argument("--processes", action="store_true")
    args = parser.parse_args()
    # Cada hilo lee un archivo independiente y devuelve su resultado al hilo principal.
    with TemporaryDirectory() as directory:
        paths = [Path(directory) / f"batch-{index}.json" for index in range(3)]
        for path, expense in zip(paths, sample_expenses(), strict=False):
            save_json([expense], path)
        with ThreadPoolExecutor(max_workers=3) as executor:
            print("Independent file totals:", list(executor.map(read_total, paths)))

    # asyncio coordina esperas sin bloquear por cada petición; el transporte usa datos simulados.
    asyncio.run(query_multiple_sources())
    if args.processes:
        # Los procesos separan trabajo de cálculo, pero añaden arranque y transferencia de datos.
        with ProcessPoolExecutor(max_workers=2) as executor:
            print("Process results:", list(executor.map(calculate_checksum, [10000, 20000])))


if __name__ == "__main__":
    main()
