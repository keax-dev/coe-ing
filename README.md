# Fundamentos de Python: nivel intermedio

Esta carpeta contiene **ejemplos independientes**, uno por tema. No es una
aplicación y no necesitas levantar un servidor. Cada archivo incluye sus propios
datos, funciones y clases; no importa código de las otras lecciones.

Todo está preparado para **Python 3.14.7**. Al inicio de cada archivo hay una sola
línea con el tema. Los comentarios explicativos están junto al código y en español;
los nombres de archivos, identificadores y mensajes están en inglés.

## Preparación

Abre la terminal en la carpeta del repositorio:

```powershell
cd C:\Users\jimen\Documents\coe-ing
```

Si ya tienes el entorno `.venv` de esta carpeta, verifica su versión e instala
las dependencias de los ejemplos:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El primer comando debe mostrar `Python 3.14.7`. Si todavía no tienes el entorno,
créalo primero con esa versión:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
```

Comprueba también que `py -3.14 --version` muestre `Python 3.14.7`.
El archivo `.python-version` indica la versión de referencia para herramientas
que reconocen ese formato. No necesitas activar el entorno si usas los comandos
anteriores.

## Cómo ejecutar un ejemplo

Ejecuta únicamente el archivo del tema que quieras estudiar:

```powershell
.\.venv\Scripts\python.exe lesson_03_lambda_and_functional_tools.py
```

El archivo muestra los resultados y termina. Puedes leer sus comentarios,
cambiar los datos y ejecutarlo otra vez. No requiere ejecutar otra lección antes.
El orden siguiente organiza los conceptos de menor a mayor complejidad.

## Temas y orden recomendado

| Orden | Archivo | Qué muestra |
| --- | --- | --- |
| 01 | `lesson_01_collections.py` | Referencias, copias superficiales y profundas, desempaquetado, comprensiones, `Counter` y `defaultdict`. |
| 02 | `lesson_02_functions.py` | Parámetros por nombre, `*args`, `**kwargs`, valores predeterminados y efectos secundarios. |
| 03 | `lesson_03_lambda_and_functional_tools.py` | `lambda`, funciones de orden superior, `sorted`, `map`, `filter`, `reduce`, `partial`, `any`, `all`, `zip` y `enumerate`. |
| 04 | `lesson_04_generators.py` | Iteradores, `yield`, evaluación diferida, consumo único e `itertools`. |
| 05 | `lesson_05_classes_and_composition.py` | `dataclass`, `Enum`, inmutabilidad, composición, encapsulación, clases abstractas y polimorfismo. |
| 06 | `lesson_06_typing.py` | Anotaciones, uniones, genéricos, `TypedDict` y `Protocol`. |
| 07 | `lesson_07_exceptions.py` | Excepciones propias, validación, encadenamiento, `else` y `finally`. |
| 08 | `lesson_08_context_managers.py` | `with`, `contextmanager`, `ExitStack` y cierre de recursos incluso ante errores. |
| 09 | `lesson_09_decorators_and_closures.py` | Cierres, decoradores, `wraps`, `ParamSpec` y medición de duración. |
| 10 | `lesson_10_files_dates_and_money.py` | JSON, CSV, rutas, fechas, `Decimal` y redondeo explícito. |
| 11 | `lesson_11_sqlite.py` | SQL parametrizado, creación, consulta, edición, eliminación y reversión de transacciones. |
| 12 | `lesson_12_http_and_validation.py` | HTTPX, Pydantic, estados HTTP, timeouts y respuestas inválidas con red simulada. |
| 13 | `lesson_13_algorithms_and_profiling.py` | Búsqueda secuencial, índices, recursividad, complejidad, `timeit` y `cProfile`. |
| 14 | `lesson_14_concurrency.py` | Hilos, tareas asíncronas, `TaskGroup` y procesos opcionales para cálculo. |
| 15 | `lesson_15_testing.py` | Pruebas con pytest, parametrización, fixtures, archivos temporales y sustitución de dependencias. |
| 16 | `lesson_16_logging.py` | Niveles de registro, manejadores, formato, filtrado y trazas de excepciones. |

## Dependencias

La mayoría de las lecciones usa únicamente la biblioteca estándar de Python.
`requirements.txt` instala las dependencias externas de estos archivos:

| Archivo | Dependencias externas |
| --- | --- |
| `lesson_12_http_and_validation.py` | HTTPX y Pydantic |
| `lesson_14_concurrency.py` | HTTPX |
| `lesson_15_testing.py` | pytest |

La instalación inicial necesita internet. Después, todos los ejemplos funcionan
sin conexión: las solicitudes HTTP utilizan respuestas simuladas.

## Archivos temporales y errores de ejemplo

Las lecciones de archivos, SQLite y concurrencia usan carpetas temporales que se
eliminan al terminar. No crean una base de datos de trabajo ni guardan información
personal. Las pruebas de archivos utilizan la carpeta temporal que administra pytest.

Algunos ejemplos provocan errores intencionalmente y los capturan para mostrar
validación, limpieza o reversión de operaciones. Un mensaje de error controlado
dentro de su salida no significa que el archivo haya fallado.

La lección de concurrencia puede mostrar también procesos separados:

```powershell
.\.venv\Scripts\python.exe lesson_14_concurrency.py --processes
```

Los ejemplos de concurrencia y los tiempos impresos sirven para entender los
mecanismos; no garantizan mejoras de velocidad para cualquier tarea.

## Ejecutar las pruebas de ejemplo

La lección de pruebas contiene tanto las funciones de ejemplo como sus propias
pruebas. Puedes ejecutarla de cualquiera de estas formas:

```powershell
.\.venv\Scripts\python.exe lesson_15_testing.py
.\.venv\Scripts\python.exe -m pytest lesson_15_testing.py -q
```

## Cómo estudiar

1. Abre el archivo del tema y lee los comentarios junto a cada bloque.
2. Predice la salida antes de ejecutarlo.
3. Ejecuta el archivo y compara el resultado con tu predicción.
4. Modifica un dato o una condición y vuelve a ejecutarlo.
5. Explica qué cambió y por qué, sin necesitar revisar otro archivo.
