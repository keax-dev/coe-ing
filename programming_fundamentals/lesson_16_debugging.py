# Tema: depuración, seguimiento de variables y lectura de errores.
# Compararemos una suma incorrecta con otra correcta usando los mismos datos.
# Un error lógico puede producir un resultado incorrecto sin lanzar una excepción.
# Una traza permite ver el valor de cada variable en cada vuelta del bucle.
# También mostraremos un traceback controlado con el archivo y la línea del error.
# Ejecuta: py lesson_16_debugging.py
# Opcional: py lesson_16_debugging.py --debug
# En el depurador usa n para avanzar, p total_cents para inspeccionar y c para continuar.

import sys
import traceback


def calculate_incorrect_total(amounts_cents):
    total_cents = 0
    for amount_cents in amounts_cents:
        # Este error es intencional: reemplaza el total en lugar de acumularlo.
        total_cents = amount_cents
        print(f"Incorrect trace: amount={amount_cents}, total={total_cents}")
    return total_cents


def calculate_traced_total(amounts_cents, debug=False):
    total_cents = 0
    for amount_cents in amounts_cents:
        previous_total_cents = total_cents
        if debug:
            # Solo detenemos la ejecución si se solicitó el modo interactivo de depuración.
            breakpoint()
        total_cents += amount_cents
        print(f"Correct trace: previous={previous_total_cents}, amount={amount_cents}, total={total_cents}")
    return total_cents


if __name__ == "__main__":
    amounts_cents = [1250, 300, 250]
    expected_total_cents = 1800
    incorrect_total_cents = calculate_incorrect_total(amounts_cents)
    correct_total_cents = calculate_traced_total(amounts_cents, debug="--debug" in sys.argv)

    print("Expected total:", expected_total_cents)
    print("Incorrect result:", incorrect_total_cents)
    print("Correct result:", correct_total_cents)

    # Leemos la última línea para identificar el tipo de error y luego buscamos su origen.
    try:
        print(amounts_cents[10])
    except IndexError:
        print("Handled error example:")
        print(traceback.format_exc(), end="")
