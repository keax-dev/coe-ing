# Patrones de Diseño en Python

Tres ejemplos sencillos e independientes, compatibles con **Python 3.14.7**.
Cada archivo contiene su propio código y muestra sus resultados al ejecutarse.
No necesitas instalar bibliotecas ni levantar un servidor.

| Patrón | Archivo | Idea del ejemplo |
| --- | --- | --- |
| Factory | `pattern_01_factory.py` | Una fábrica simple crea una notificación de correo o SMS según el canal recibido. |
| Strategy | `pattern_02_strategy.py` | Un calculador cambia entre envío estándar y exprés intercambiando el algoritmo. |
| Observer | `pattern_03_observer.py` | Un publicador avisa a sus suscriptores y permite cancelar suscripciones. |

Factory se muestra mediante la variante de fábrica simple: una función centraliza
la selección y construcción del objeto. Los envíos y notificaciones son simulados;
los ejemplos únicamente imprimen mensajes. Las tarifas son valores ilustrativos.

## Ejecución

Desde la raíz del repositorio:

```powershell
py -3.14 --version
py -3.14 pattern_01_factory.py
py -3.14 pattern_02_strategy.py
py -3.14 pattern_03_observer.py
```

Comprueba que la versión sea `Python 3.14.7`. También puedes usar el entorno
virtual existente:

```powershell
.\.venv\Scripts\python.exe pattern_01_factory.py
```

## Qué observar

- **Factory:** el consumidor pide un canal y recibe un objeto con el método `send`.
- **Strategy:** el mismo calculador devuelve `6` con envío estándar y `12` con exprés para un peso de `3`.
- **Observer:** Alex y Sam reciben la primera noticia; solo Sam recibe la segunda.

Al inicio de cada archivo hay una sola línea con el tema. Los comentarios
explicativos están junto al código y en español; los identificadores, nombres
de archivos y mensajes están en inglés.
