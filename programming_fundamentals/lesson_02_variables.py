# Tema: variables, tipos de datos y conversiones.
# Representaremos un gasto con texto, enteros, decimales, booleanos y ausencia de valor.
# Las variables son nombres asociados a valores; pueden reasignarse.
# Usaremos centavos enteros para almacenar dinero sin errores de punto flotante.
# Ejecuta: python lesson_02_variables.py

if __name__ == "__main__":
    description = "Lunch"
    amount_cents = 1250
    display_amount = amount_cents / 100
    is_paid = True
    receipt = None

    print("Description:", description, type(description).__name__)
    print("Amount in cents:", amount_cents, type(amount_cents).__name__)
    print("Display amount:", display_amount, type(display_amount).__name__)
    print("Paid:", is_paid, type(is_paid).__name__)
    print("Receipt:", receipt, type(receipt).__name__)

    # La entrada del usuario es texto; convertirla permite hacer cálculos.
    raw_amount = "1500"
    amount_cents = int(raw_amount)
    print("Updated amount:", amount_cents)
    print("Amount as text:", str(amount_cents))
    print("Decimal from text:", float("15.50"))

    # Python permite cambiar de tipo, pero mantener el propósito de cada nombre ayuda.
    receipt = "receipt_001.pdf"
    print("Receipt attached:", receipt is not None)

# Práctica:
# 1. Crea variables para el presupuesto, la categoría y si el gasto es recurrente.
# 2. Cambia raw_amount por texto no numérico y observa el error de conversión.
# 3. Comprueba con type() el resultado de dividir dos enteros con /.
