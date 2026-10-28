# Python intermedio aplicado: registro de gastos

Curso práctico de 16 lecciones para quienes ya conocen variables, tipos básicos,
condicionales, bucles, entrada/salida y funciones sencillas. El proyecto evoluciona
hasta una aplicación de terminal con modelos, cálculos monetarios exactos,
persistencia SQLite, validación externa y pruebas automatizadas.

Cada archivo Python comienza con una sola línea que indica el tema. Las explicaciones
en español aparecen junto al código que describen. Los archivos,
identificadores y mensajes del programa están en inglés. Las lecciones están en la
raíz de esta rama, sin una carpeta adicional que las contenga.

## Instalación en Windows

El proyecto está configurado y verificado con **Python 3.14.7**. Necesitas internet
para la instalación inicial. El archivo `.python-version` indica la versión de
referencia y `pyproject.toml` requiere Python 3.14 desde el parche 3.14.7.
Desde la raíz del repositorio, ejecuta:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe lesson_01_project_structure.py
```

La instalación editable conecta los archivos de `src/` con el entorno virtual.
Puedes modificar el paquete sin reinstalarlo. Si cambias las dependencias o los
comandos de `pyproject.toml`, vuelve a ejecutar la instalación. No necesitas activar
el entorno: estos comandos usan su intérprete directamente.

Comprueba que el primer comando muestre `Python 3.14.7`. Si ya tienes un entorno
virtual, verifica también su versión con `.\.venv\Scripts\python.exe --version`.
Ruff y mypy están configurados para analizar código de Python 3.14.

En Linux o macOS usa Python 3.14.7, crea el entorno con
`python3.14 -m venv .venv` y utiliza
`.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`.

## Orden de estudio

| Orden | Archivo | Conceptos y aplicación |
| --- | --- | --- |
| 01 | `lesson_01_project_structure.py` | Paquetes, instalación editable, dependencias y separación de responsabilidades. |
| 02 | `lesson_02_collection_semantics.py` | Mutabilidad, referencias, copias, desempaquetado, comprensiones, `Counter` y `defaultdict`. |
| 03 | `lesson_03_function_contracts.py` | Parámetros por nombre, `*args`, `**kwargs`, argumentos mutables y efectos secundarios. |
| 04 | `lesson_04_functional_tools.py` | `lambda`, funciones de orden superior, `map`, `filter`, `reduce`, `partial`, `sorted`, `any`, `all`, `zip` y `enumerate`. |
| 05 | `lesson_05_iterators_and_generators.py` | Iterables, iteradores, `yield`, consumo único, evaluación diferida e `itertools`. |
| 06 | `lesson_06_object_modeling.py` | `dataclass`, `Enum`, composición, encapsulación, inmutabilidad, métodos especiales y herencia con clases abstractas. |
| 07 | `lesson_07_type_contracts.py` | Anotaciones, uniones, `TypedDict`, genéricos, `Protocol` y análisis estático con mypy. |
| 08 | `lesson_08_errors_and_contexts.py` | Excepciones propias, encadenamiento, administradores de contexto y `logging`. |
| 09 | `lesson_09_automated_testing.py` | pytest, fixtures, parametrización, archivos temporales y simulación de dependencias. |
| 10 | `lesson_10_decorators_and_closures.py` | Cierres, fábricas de funciones, decoradores, `wraps`, `ParamSpec` y medición de duración. |
| 11 | `lesson_11_files_dates_and_money.py` | `pathlib`, JSON, CSV, fechas, `Decimal`, redondeo explícito y validación al importar. |
| 12 | `lesson_12_sqlite_persistence.py` | Repositorios, consultas parametrizadas, CRUD y transacciones con reversión. |
| 13 | `lesson_13_http_and_validation.py` | HTTPX, timeouts, estados HTTP, errores de red y validación de respuestas con Pydantic. |
| 14 | `lesson_14_algorithms_and_profiling.py` | Búsqueda, índices, recursividad, complejidad temporal y espacial, `timeit` y `cProfile`. |
| 15 | `lesson_15_concurrency.py` | Hilos para archivos, `asyncio`, `TaskGroup`, clientes asíncronos y procesos para cálculo. |
| 16 | `lesson_16_integrated_application.py` | Integración con `argparse`, persistencia, reportes, importación/exportación y códigos de salida. |

Ejecuta cada archivo con el intérprete del entorno virtual. Por ejemplo:

```powershell
.\.venv\Scripts\python.exe lesson_04_functional_tools.py
.\.venv\Scripts\python.exe lesson_12_sqlite_persistence.py
.\.venv\Scripts\python.exe lesson_16_integrated_application.py
```

Las demostraciones usan datos reproducibles y carpetas temporales, sin escribir en
tu base de datos de trabajo. Las lecciones 13 y 15 simulan las respuestas HTTP:
no necesitan internet en su modo normal.

La lección 13 acepta `--url` para consultar un endpoint real con este contrato:
`{"base": "USD", "rates": {"EUR": "0.92"}}`. Las tasas del ejemplo son ficticias.
La lección 15 acepta `--processes` para mostrar procesos separados. Los ejemplos
de concurrencia no prometen mayor velocidad: depende del tipo y tamaño del trabajo.

## Estructura del proyecto

```text
coe-ing/
    lesson_01_project_structure.py
    ...
    lesson_16_integrated_application.py
    pyproject.toml
    README.md
    src/
        expense_tracker/
            models.py
            services.py
            repositories.py
            serialization.py
            rates.py
            instrumentation.py
            cli.py
            ...
    tests/
        conftest.py
        test_models.py
        test_services.py
        test_storage.py
        test_rates.py
        test_cli.py
        test_instrumentation.py
        test_lessons.py
```

Las lecciones muestran un tema por archivo. `src/expense_tracker` contiene las
implementaciones compartidas que usa la aplicación real; `tests/` comprueba su
comportamiento. Lee los módulos importados cuando una lección los utilice.
Las anotaciones aparecen desde el inicio para mantener contratos consistentes;
la lección 07 las explica en detalle.

## Herramientas y bibliotecas

| Herramienta | Uso |
| --- | --- |
| Biblioteca estándar | Colecciones, tipos, fechas, archivos, SQLite, contexto, registros, perfilado, concurrencia y terminal. |
| HTTPX | Solicitudes HTTP síncronas y asíncronas; respuestas simuladas. |
| Pydantic | Validación de las respuestas externas antes de usarlas. |
| pytest | Pruebas unitarias, integración, fixtures y parametrización. |
| Ruff | Revisión del código, organización de importaciones y formato. |
| mypy | Comprobación estática estricta del paquete en `src/`. |

Las herramientas de desarrollo se instalan con el extra `[dev]`.
`pyproject.toml` declara los rangos de versiones compatibles del proyecto.

## Aplicación de terminal

Los montos se ingresan en dólares como texto decimal: `12.50` representa
doce dólares con cincuenta centavos. El modelo usa `Decimal` para preservar
los valores monetarios exactos.

```powershell
.\.venv\Scripts\python.exe -m expense_tracker add "Team lunch" 12.50 --category food --date 2026-10-01
.\.venv\Scripts\python.exe -m expense_tracker add "Bus" 3.00 --category transport
.\.venv\Scripts\python.exe -m expense_tracker list
.\.venv\Scripts\python.exe -m expense_tracker summary --budget 50.00
.\.venv\Scripts\python.exe -m expense_tracker export-json data/backup.json
```

Las categorías son `food`, `transport`, `education` y `other`.
El comando `list` muestra el ID completo que puedes usar con `update` y `delete`:

```powershell
.\.venv\Scripts\python.exe -m expense_tracker update EXPENSE_ID "Updated description"
.\.venv\Scripts\python.exe -m expense_tracker delete EXPENSE_ID
```

Reemplaza `EXPENSE_ID` por un ID real. Consulta las opciones con
`.\.venv\Scripts\python.exe -m expense_tracker --help`.

La aplicación guarda cada cambio inmediatamente en `data/expenses.db`, relativo
a la carpeta desde la que la ejecutes. El presupuesto de `summary` es un parámetro
del reporte y no se guarda. Los gastos pueden superar el presupuesto y producir
un saldo negativo. La lección 06 muestra una política alternativa que los rechaza.

Para elegir otra base de datos, coloca `--database` antes del subcomando:

```powershell
.\.venv\Scripts\python.exe -m expense_tracker --database data/restored.db import-json data/backup.json
```

La importación agrega registros en una transacción. Si un ID ya existe, se revierte
toda la importación. El archivo debe seguir el esquema exportado por esta versión.
Los archivos de `data/` y el entorno virtual están excluidos de Git.

## Verificación

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
.\.venv\Scripts\python.exe -m mypy src
```

Las pruebas verifican montos, filtros, aislamiento de datos, archivos, transacciones,
HTTP simulado y comandos de terminal. También ejecutan cada lección en su modo
normal. La lección 09 ejecuta solo las pruebas de modelos y servicios para evitar
que las pruebas de ejecución se invoquen a sí mismas.

## Forma de estudio

1. Lee el tema y los comentarios del código; predice el resultado antes de ejecutar el archivo.
2. Sigue el flujo desde la lección hasta los módulos que importa.
3. Cambia los datos o una regla y observa qué resultados y pruebas se ven afectados.
4. Explica las decisiones: mutabilidad, responsabilidades, contratos y manejo de fallos.
5. Usa los comandos de la aplicación para comprobar cómo se integran los conceptos.

## Documentación de referencia

- [Biblioteca estándar de Python](https://docs.python.org/3/library/index.html)
- [pytest](https://docs.pytest.org/en/stable/)
- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/en/stable/)
- [HTTPX y transportes simulados](https://www.python-httpx.org/advanced/transports/)
- [Pydantic](https://docs.pydantic.dev/latest/)
