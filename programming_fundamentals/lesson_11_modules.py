# Tema: módulos, importaciones y biblioteca estándar.
# Cada archivo .py puede funcionar como módulo y compartir sus funciones.
# Importaremos funciones de la lección anterior y utilidades incluidas en Python.
# No hace falta instalar paquetes externos para este proyecto.
# Un paquete organiza varios módulos; aquí usaremos módulos en una misma carpeta.
# Ejecuta: python lesson_11_modules.py

from datetime import date
from pathlib import Path

from lesson_10_functions import calculate_total, create_expense, format_money


if __name__ == "__main__":
    expenses = [create_expense("Lunch", 1250, "food")]
    today = date.today()
    project_directory = Path(__file__).resolve().parent

    print("Report date:", today.isoformat())
    print("Project directory:", project_directory)
    print("Total:", format_money(calculate_total(expenses)))

    # Al importar la lección 10, su bloque principal no se ejecuta.
    # Así reutilizamos funciones sin imprimir su demostración.

# Práctica:
# 1. Importa calculate_balance y muestra un saldo.
# 2. Mueve una función nueva a otro archivo e impórtala aquí.
# 3. Ejecuta directamente la lección 10 y compara su salida con la de este archivo.
