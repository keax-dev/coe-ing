# Tema: manejo de errores y depuración mediante trazas e inspección de variables.

import sys
import traceback


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


def calculate_total(scores: list[int], *, debug: bool = False) -> int:
    total = 0
    for score in scores:
        previous_total = total
        if debug:
            # Con --debug puedes avanzar con n, inspeccionar con p total y continuar con c.
            breakpoint()
        total += score
        print(f"Trace: previous={previous_total}, score={score}, total={total}")
    return total


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

    scores = [70, 80, 90]
    incorrect_total = 0
    for score in scores:
        # Error lógico intencional: reemplazar el acumulado deja únicamente el último valor.
        incorrect_total = score
    print("Incorrect total:", incorrect_total)
    print("Correct total:", calculate_total(scores, debug="--debug" in sys.argv))

    try:
        parse_score("invalid")
    except ScoreError:
        # La última línea identifica el error; las anteriores muestran dónde se originó.
        print("Handled traceback example:")
        print(traceback.format_exc(), end="")


if __name__ == "__main__":
    main()
