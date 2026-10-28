# Tema: validación y manejo de excepciones.
# Convertiremos montos escritos por el usuario y rechazaremos datos inválidos.
# raise comunica un error; try y except permiten responder sin cerrar el programa.
# else se ejecuta si no hubo error; finally se ejecuta en ambos casos.
# Ejecuta: python lesson_12_exceptions.py

from lesson_10_functions import format_money


def parse_amount(raw_amount):
    amount_cents = int(raw_amount)
    if amount_cents <= 0:
        raise ValueError("Amount must be a positive integer in cents.")
    return amount_cents


if __name__ == "__main__":
    for raw_amount in ["1250", "hello", "-300", "0", "450"]:
        print("Input:", raw_amount)
        try:
            amount_cents = parse_amount(raw_amount)
        except ValueError as error:
            print("Invalid amount:", error)
        else:
            print("Accepted:", format_money(amount_cents))
        finally:
            print("Validation finished.")

# Práctica:
# 1. Agrega entradas vacías y con decimales a los ejemplos.
# 2. Crea una función que rechace descripciones vacías con ValueError.
# 3. Combina input() con parse_amount() y vuelve a pedir el dato si es inválido.
