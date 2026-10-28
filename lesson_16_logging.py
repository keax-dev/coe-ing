# Tema: registros de ejecución, niveles de severidad y captura de errores.

import logging
from io import StringIO


def divide_scores(total: int, count: int, logger: logging.Logger) -> float | None:
    # Los argumentos separados del mensaje permiten aplazar su formato hasta que se emita.
    logger.debug("Calculating average: total=%s, count=%s", total, count)
    try:
        result = total / count
    except ZeroDivisionError:
        # exception añade la traza del error al registro dentro de un bloque except.
        logger.exception("Cannot calculate an average without scores")
        return None
    logger.info("Average calculated: %.2f", result)
    return result


def main() -> None:
    logger = logging.getLogger("logging_example")
    logger.setLevel(logging.DEBUG)
    # Desactivamos la propagación para no duplicar mensajes mediante manejadores superiores.
    logger.propagate = False
    with StringIO() as output:
        handler = logging.StreamHandler(output)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        try:
            divide_scores(270, 3, logger)
            logger.warning("A score is pending review.")
            divide_scores(0, 0, logger)
            print("Captured INFO and higher records:")
            print(output.getvalue(), end="")
            # El nivel del manejador filtra DEBUG aunque el logger sí permita ese nivel.
            print(
                "DEBUG record filtered:", "Calculating average" not in output.getvalue()
            )
        finally:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    main()
