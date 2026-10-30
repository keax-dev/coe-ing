# Fundamentos de Programación

Ejemplos prácticos independientes para **Python 3.14.7**, organizados únicamente
en estos seis temas:

| Tema | Archivo | Contenido |
| --- | --- | --- |
| Funciones | `lesson_01_functions.py` | Parámetros, retornos, argumentos nombrados, `*args`, `**kwargs`, funciones como argumentos y efectos secundarios. |
| Arreglos y colecciones | `lesson_02_arrays_and_collections.py` | Arreglos numéricos, listas, tuplas, conjuntos, diccionarios, copias, comprensiones y matrices. |
| Programación Orientada a Objetos (POO) | `lesson_03_object_oriented_programming.py` | Clases, objetos, encapsulación, composición, herencia, polimorfismo e inmutabilidad. |
| Estructuras de datos | `lesson_04_data_structures.py` | Pilas, colas, colas de prioridad y representación y recorrido de grafos. |
| Manejo de errores y depuración | `lesson_05_errors_and_debugging.py` | Excepciones, validación, encadenamiento, trazas de errores, errores lógicos e inspección paso a paso. |
| Buenas prácticas de desarrollo | `lesson_06_development_practices.py` | Nombres descriptivos, constantes, responsabilidades, funciones puras, tipos, separación de cálculo y salida, y pruebas. |

Cada archivo contiene todo lo necesario para ejecutar sus ejemplos y no importa
código de otras lecciones. Al inicio hay una sola línea con el tema; las
explicaciones están junto al código y en español. Los identificadores y mensajes
del programa están en inglés.

## Ejecución

Desde la raíz del repositorio, ejecuta cualquiera de los archivos:

```powershell
py -3.14 --version
py -3.14 lesson_01_functions.py
py -3.14 lesson_02_arrays_and_collections.py
```

Comprueba que la versión sea `Python 3.14.7`. Si prefieres usar el entorno virtual
existente, puedes ejecutar:

```powershell
.\.venv\Scripts\python.exe lesson_03_object_oriented_programming.py
```

**No necesitas instalar dependencias:** todos los ejemplos usan la biblioteca
estándar de Python. No hay aplicación, servidor ni base de datos que levantar.

## Depuración y comprobaciones

El archivo de errores muestra fallos controlados y un cálculo incorrecto
intencional, seguido de la solución. Para inspeccionar el cálculo paso a paso:

```powershell
py -3.14 lesson_05_errors_and_debugging.py --debug
```

En el depurador usa `n` para avanzar, `p total` para inspeccionar el acumulador
y `c` para continuar.

Las pruebas de ejemplo están dentro del tema de buenas prácticas. Ejecútalas con:

```powershell
py -3.14 lesson_06_development_practices.py --check
```

## Forma de estudio

1. Abre el archivo y lee sus comentarios.
2. Predice el resultado y ejecuta el ejemplo.
3. Modifica un dato o una condición y compara la nueva salida.
4. Explica el comportamiento sin depender de otra lección.
