# Tema: repetición con while, contadores y condiciones de salida.
# Procesaremos gastos hasta que ya no alcancen los fondos.
# Un while debe modificar algo que permita terminar; de lo contrario puede ser infinito.
# El modo interactivo agrega un menú pequeño que termina con la opción 0.
# Ejecuta: python lesson_07_while_loops.py

import sys

if __name__ == "__main__":
    balance_cents = 2000
    daily_cost_cents = 600
    day_count = 0

    while balance_cents >= daily_cost_cents:
        balance_cents -= daily_cost_cents
        day_count += 1
        print(f"Day {day_count}: balance = {balance_cents} cents")
    print("Days covered:", day_count)

    if "--interactive" in sys.argv:
        is_running = True
        while is_running:
            choice = input("1. View balance | 0. Exit: ").strip()
            if choice == "1":
                print("Balance cents:", balance_cents)
            elif choice == "0":
                is_running = False
            else:
                print("Unknown option.")

# Práctica:
# 1. Cambia el costo diario y predice cuántas vueltas realizará el bucle.
# 2. Agrega al menú una opción para restablecer el saldo a 2000.
# 3. Explica qué pasaría si eliminas la resta dentro del primer while.
