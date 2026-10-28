# Fundamentos de programación: registro de gastos

Construye un registro de gastos paso a paso con la biblioteca estándar de Python.
Cada lección se ejecuta de forma independiente con datos de ejemplo. Lee los
comentarios en español, ejecuta el código, cambia los valores y compara los
escenarios. Los identificadores del código y los mensajes del programa están en inglés.

## Requisitos

Python 3.10 o superior. No se necesitan paquetes externos.

## Ejecución

Abre una terminal en esta carpeta y ejecuta:

```powershell
python lesson_01_first_program.py
python lesson_02_variables.py
```

Continúa en el orden de la tabla. Si tu instalación utiliza `py`, reemplaza
`python` por `py` en estos comandos.

| Archivo | Qué aprenderás |
| --- | --- |
| `lesson_01_first_program.py` | Instrucciones, orden de ejecución, sangría y salida de datos |
| `lesson_02_variables.py` | Variables, tipos, reasignación y conversiones |
| `lesson_03_operators.py` | Aritmética, comparaciones, lógica, asignación y precedencia |
| `lesson_04_input_output.py` | Entrada del usuario, conversión y salida con formato |
| `lesson_05_conditionals.py` | Decisiones con `if`, `elif` y `else` |
| `lesson_06_for_loops.py` | Iteración, `range`, `break`, `continue` y `pass` |
| `lesson_07_while_loops.py` | Repetición, contadores y condiciones de salida |
| `lesson_08_collections.py` | Listas, tuplas, diccionarios, conjuntos y comprensiones |
| `lesson_09_strings.py` | Limpieza, búsqueda, segmentación y formato de texto |
| `lesson_10_functions.py` | Parámetros, retornos, valores predeterminados y alcance de variables |
| `lesson_11_modules.py` | Importaciones, biblioteca estándar y reutilización de código |
| `lesson_12_exceptions.py` | Validación, `raise`, `try`, `except`, `else` y `finally` |
| `lesson_13_files.py` | Archivos de texto, JSON, administradores de contexto y rutas |
| `lesson_14_expense_tracker.py` | Proyecto integrador con menú y almacenamiento de gastos |
| `lesson_15_algorithm_design.py` | Entradas, procesamiento, salidas y pasos de un algoritmo |
| `lesson_16_debugging.py` | Errores lógicos, seguimiento de ejecución, trazas de errores y depurador |
| `lesson_17_references_and_copies.py` | Mutabilidad, identidad y copias superficiales y profundas |
| `lesson_18_searching_and_sorting.py` | Búsqueda secuencial, filtrado y ordenamiento por una clave |
| `lesson_19_statistics.py` | Contadores, acumuladores, promedios, mínimo y máximo |
| `lesson_20_nested_loops.py` | Datos anidados, bucles anidados e informes mensuales por categoría |
| `lesson_21_testing.py` | Pruebas automatizadas, resultados esperados y casos límite |
| `lesson_22_function_behavior.py` | Efectos secundarios, argumentos mutables y valores predeterminados seguros |

Las lecciones 15 a 22 amplían el registro de gastos mediante ejemplos de cada tema.
Se ejecutan de forma independiente y reutilizan algunas funciones de las lecciones
anteriores. La lección 16 muestra intencionalmente un cálculo incorrecto y un error
controlado, y después presenta el cálculo corregido. La lección 22 demuestra un
valor predeterminado mutable compartido antes de mostrar la alternativa segura.

Ejecuta las lecciones adicionales y sus comprobaciones automatizadas:

```powershell
py lesson_15_algorithm_design.py
py lesson_21_testing.py
py lesson_22_function_behavior.py
```

Para depurar paso a paso, ejecuta `py lesson_16_debugging.py --debug`.
En el depurador, usa `n` para avanzar, `p total_cents` para inspeccionar el
acumulador y `c` para continuar.

Las lecciones 04 y 07 tienen modos interactivos opcionales:

```powershell
python lesson_04_input_output.py --interactive
python lesson_07_while_loops.py --interactive
```

El proyecto integrador también comienza con una demostración de ejemplo de forma predeterminada:

```powershell
python lesson_14_expense_tracker.py
python lesson_14_expense_tracker.py --interactive
```

En el modo interactivo puedes agregar gastos, listarlos, consultar totales y guardar
o cargar registros. Al guardar, se escribe en `data/expenses.json`, junto a los
archivos de las lecciones. La carga reemplaza los registros de la sesión actual.
Guarda antes de salir si quieres conservar los cambios. Las demostraciones usan
archivos temporales y no modifican tus registros guardados.

## Forma de estudio

1. Lee los comentarios iniciales de una lección.
2. Predice la salida antes de ejecutarla.
3. Ejecuta la lección y compara el resultado con tu predicción.
4. Cambia una entrada o condición y vuelve a ejecutarla para comprobar tu predicción.
5. Usa el proyecto integrador para ver cómo se combinan los conceptos.

Los montos se almacenan como centavos enteros: `1250` representa `12.50`.
Esto mantiene los cálculos exactos mientras practicas los tipos de datos básicos.
