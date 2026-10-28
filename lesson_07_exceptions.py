# Tema: excepciones propias, validación y encadenamiento de errores.


class ScoreError(ValueError):
    pass


def parse_score(raw_score: str) -> int:
    try:
        score = int(raw_score)
    except ValueError as error:
        # Traducimos un error técnico a uno del dominio y conservamos la causa original.
        raise ScoreError("Score must be an integer.") from error
    if not 0 <= score <= 100:
        raise ScoreError("Score must be between 0 and 100.")
    return score


def main() -> None:
    for raw_score in ["85", "invalid", "120"]:
        print("Input:", raw_score)
        try:
            score = parse_score(raw_score)
        except ScoreError as error:
            # Capturamos solo el fallo que sabemos manejar, sin ocultar errores inesperados.
            print("Rejected:", error)
            if error.__cause__ is not None:
                print("Original error:", type(error.__cause__).__name__)
        else:
            # else separa el camino exitoso del código que puede fallar.
            print("Accepted:", score)
        finally:
            # finally se ejecuta tanto si la conversión tuvo éxito como si fue rechazada.
            print("Validation finished.")


if __name__ == "__main__":
    main()
