# Tema: limpieza, búsqueda, segmentación y formato de cadenas.
# Normalizaremos datos para evitar categorías duplicadas por espacios o mayúsculas.
# Las cadenas son inmutables: sus métodos devuelven nuevas cadenas.
# Ejecuta: python lesson_09_strings.py

if __name__ == "__main__":
    raw_description = "  morning COFFEE  "
    description = raw_description.strip().title()
    category = " FOOD ".strip().lower()

    print("Original:", repr(raw_description))
    print("Clean description:", description)
    print("Clean category:", category)
    print("Contains coffee:", "coffee" in description.lower())
    print("First seven characters:", description[:7])
    print("Updated description:", description.replace("Coffee", "Tea"))

    raw_tags = "work, food, morning"
    tags = [tag.strip() for tag in raw_tags.split(",")]
    print("Tags:", tags)
    print("Joined tags:", " | ".join(tags))

    amount_cents = 1250
    print(f"{description:<20} ${amount_cents // 100}.{amount_cents % 100:02d}")

# Práctica:
# 1. Normaliza una categoría escrita con espacios y mayúsculas.
# 2. Rechaza una descripción que quede vacía después de strip().
# 3. Divide una lista de categorías separadas por comas y vuelve a unirla.
