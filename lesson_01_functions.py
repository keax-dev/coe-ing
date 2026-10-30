# Tema: funciones, parámetros, retornos y funciones como argumentos.

from collections.abc import Callable, Iterable


def average_score(scores: Iterable[int], *, minimum: int = 0) -> float | None:
    # El asterisco exige pasar minimum por nombre; la función no modifica la entrada.
    selected = [score for score in scores if score >= minimum]
    return sum(selected) / len(selected) if selected else None


def combine_names(*groups: Iterable[str]) -> list[str]:
    # *groups reúne varias colecciones; los recorridos anidados las aplanan.
    return [name for group in groups for name in group]


def build_profile(**fields: str) -> dict[str, str]:
    # **fields captura argumentos nombrados y los transforma en un diccionario.
    return {key: value.strip() for key, value in fields.items()}


def with_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    # None evita compartir una lista predeterminada; devolvemos otra lista sin alterar la recibida.
    return [*(tags if tags is not None else []), tag]


def append_tag(tag: str, tags: list[str]) -> None:
    # Esta alternativa sí modifica el objeto del llamador: tiene un efecto secundario.
    tags.append(tag)


def transform_scores(
    scores: Iterable[int], transform: Callable[[int], int]
) -> list[int]:
    # Recibir una función permite reutilizar el recorrido con diferentes transformaciones.
    return [transform(score) for score in scores]


def main() -> None:
    print("Selected average:", average_score([60, 85, 95], minimum=80))
    print("Empty average:", average_score([]))
    print("Combined names:", combine_names(["Alex"], ["Sam", "Taylor"]))
    print("Profile:", build_profile(name=" Alex ", language=" Python "))
    original = ["python"]
    updated = with_tag("sql", original)
    print("Original and independent result:", original, updated)
    append_tag("testing", original)
    print("Original after in-place change:", original)
    print("Independent default lists:", with_tag("first") is not with_tag("second"))
    # Una lambda expresa una función breve que devuelve una sola expresión.
    print(
        "Adjusted scores:",
        transform_scores([70, 80, 95], lambda score: min(score + 5, 100)),
    )


if __name__ == "__main__":
    main()
