# Tema: administradores de contexto y cierre garantizado de recursos.

from collections.abc import Iterator
from contextlib import ExitStack, contextmanager
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory


@contextmanager
def managed_buffer() -> Iterator[StringIO]:
    buffer = StringIO()
    print("Buffer opened.")
    try:
        # El cuerpo del with se ejecuta mientras la función queda suspendida en yield.
        yield buffer
    finally:
        # Cerramos el recurso incluso si el consumidor lanza una excepción.
        buffer.close()
        print("Buffer closed:", buffer.closed)


def main() -> None:
    with managed_buffer() as buffer:
        buffer.write("Python context example")
        print("Buffered text:", buffer.getvalue())

    try:
        with managed_buffer() as buffer:
            buffer.write("Partial result")
            raise ValueError("Simulated operation failure")
    except ValueError as error:
        print("Handled failure after cleanup:", error)

    # TemporaryDirectory elimina estos archivos al terminar la demostración.
    with TemporaryDirectory() as directory:
        paths = [Path(directory) / name for name in ["first.txt", "second.txt"]]
        for path in paths:
            path.write_text(path.stem, encoding="utf-8")
        # ExitStack administra una cantidad de recursos que solo conocemos en ejecución.
        with ExitStack() as stack:
            files = [stack.enter_context(path.open(encoding="utf-8")) for path in paths]
            print("File contents:", [file.read() for file in files])
        print("All files closed:", all(file.closed for file in files))


if __name__ == "__main__":
    main()
