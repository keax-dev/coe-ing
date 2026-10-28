# Tema: entrada, conversión y salida de datos.
# Capturaremos un gasto con input() y construiremos un comprobante con cadenas formateadas.
# input() siempre devuelve texto. int() permite convertir centavos a entero.
# La ejecución normal usa datos de ejemplo; --interactive permite escribirlos.
# En esta etapa introduce enteros válidos; en la lección 12 manejaremos errores.
# Ejecuta: python lesson_04_input_output.py --interactive

import sys

if __name__ == "__main__":
    if "--interactive" in sys.argv:
        description = input("Description: ").strip()
        raw_amount = input("Amount in cents (example: 1250): ")
    else:
        description = "Lunch"
        raw_amount = "1250"

    amount_cents = int(raw_amount)
    print("--- RECEIPT ---")
    print(f"Description: {description}")
    print(f"Amount: ${amount_cents // 100}.{amount_cents % 100:02d}")
    print("Description", "Amount (cents)", sep=" | ")
    print(description, amount_cents, sep=" | ")

# Práctica:
# 1. Pide también la categoría del gasto.
# 2. Agrega la categoría al comprobante mediante una cadena con prefijo f.
# 3. Ejecuta el archivo con y sin --interactive y compara ambos modos.
