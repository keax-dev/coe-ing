# Tema: hilos para entrada/salida, tareas asíncronas y procesos para cálculo.

import argparse
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

import httpx


def read_word_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").split())


def calculate_checksum(limit: int) -> int:
    # Una función de nivel superior puede importarse al crear procesos nuevos en Windows.
    return sum(number * number for number in range(limit))


async def simulate_response(request: httpx.Request) -> httpx.Response:
    # Cedemos el control a otra tarea sin consultar una red real.
    await asyncio.sleep(0)
    return httpx.Response(200, json={"source": request.url.path, "status": "ready"})


async def fetch_status(client: httpx.AsyncClient, source: str) -> str:
    # await evita bloquear el flujo asíncrono mientras se espera la respuesta.
    response = await client.get(f"https://status.example.test/{source}")
    response.raise_for_status()
    return f"{source}: {response.json()['status']}"


async def inspect_sources() -> None:
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(simulate_response), timeout=5.0
    ) as client:
        # TaskGroup espera todas las tareas y cancela las restantes si alguna falla.
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(fetch_status(client, source))
                for source in ["first", "second"]
            ]
        print("Async results:", [task.result() for task in tasks])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run independent concurrency examples."
    )
    parser.add_argument("--processes", action="store_true")
    args = parser.parse_args()
    with TemporaryDirectory() as directory:
        paths = [Path(directory) / f"sample-{number}.txt" for number in range(3)]
        for path, text in zip(paths, ["one", "one two", "one two three"], strict=True):
            path.write_text(text, encoding="utf-8")
        # Los hilos leen archivos independientes; el hilo principal reúne sus resultados.
        with ThreadPoolExecutor(max_workers=3) as executor:
            print("Word counts:", list(executor.map(read_word_count, paths)))
    asyncio.run(inspect_sources())
    if args.processes:
        # Los procesos separan cálculo; su arranque y transferencia de datos también tienen costo.
        with ProcessPoolExecutor(max_workers=2) as executor:
            print(
                "Process results:",
                list(executor.map(calculate_checksum, [10000, 20000])),
            )


# La protección evita iniciar más procesos al importar el archivo en un proceso trabajador.
if __name__ == "__main__":
    main()
