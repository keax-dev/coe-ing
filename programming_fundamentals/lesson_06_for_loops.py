# Tema: repetición con for, range(), break, continue y pass.
# Recorreremos gastos y acumularemos sus montos sin repetir instrucciones a mano.
# continue salta a la siguiente vuelta; break termina el bucle.
# pass no hace nada: sirve como marcador de una parte pendiente.
# Ejecuta: python lesson_06_for_loops.py

if __name__ == "__main__":
    amounts_cents = [1250, 300, 0, 450]
    total_cents = 0

    for amount_cents in amounts_cents:
        if amount_cents <= 0:
            continue
        total_cents += amount_cents
        print("Accepted cents:", amount_cents)
    print("Total cents:", total_cents)

    for day in range(1, 6):
        print(f"Day {day}: review expenses")

    for amount_cents in amounts_cents:
        if amount_cents > 1000:
            print("First expense above threshold:", amount_cents)
            break

    # Este marcador no interrumpe el bucle ni evita el print posterior.
    for category in ["food", "transport"]:
        if category == "transport":
            pass
        print("Reviewed category:", category)

# Práctica:
# 1. Cuenta cuántos gastos válidos hay, además de sumarlos.
# 2. Cambia el umbral de búsqueda y observa cuándo se ejecuta break.
# 3. Sustituye pass por un mensaje para la categoría transport.
