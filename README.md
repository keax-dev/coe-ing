# Componentes backend: instituciones y educación

API de FastAPI con **Python 3.14.7** y persistencia en un archivo **SQLite**.
No necesitas instalar un servidor de base de datos, un gestor gráfico ni contenedores.

- Instituciones: arquitectura hexagonal en `src/institution/hexagonal`.
- Educación: Clean Architecture en `src/education/clean`.
- Ambos CRUD incluyen borrado lógico, control de versión y validación de datos.

El código usa identificadores y mensajes en inglés; los comentarios y la
documentación están en español. [ARCHITECTURE.md](ARCHITECTURE.md) explica las capas.

## 1. Obtener el proyecto

Si todavía no tienes el repositorio:

```powershell
git clone --branch backend_component_architecture https://github.com/keax-dev/coe-ing.git
cd coe-ing
```

Si ya lo tienes, abre una terminal en su raíz y selecciona la rama
`backend_component_architecture`. Los siguientes comandos se ejecutan desde esa carpeta.

## 2. Preparar Python e instalar dependencias

Instala Python **3.14.7** y verifica la versión:

```powershell
py -3.14 --version
```

Crea el entorno virtual e instala las dependencias:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

No hace falta activar el entorno: los comandos usan su intérprete directamente.
Si `.venv` ya existe, verifica su versión con
`.\.venv\Scripts\python.exe --version` y ejecuta solo la instalación.

## 3. Configurar el archivo de datos

Crea `.env` si aún no existe:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Su única variable es:

```dotenv
DB_URL=sqlite:///./data/portfolio.db
```

Este también es el valor predeterminado si no configuras `DB_URL`. La carpeta
`data/` se crea automáticamente. Las variables del sistema tienen prioridad sobre
`.env`; si cambias la URL, la API utilizará otro archivo.

Las rutas relativas se resuelven desde la carpeta de ejecución: utiliza siempre
la raíz del repositorio. No hay usuario, contraseña ni driver externo que configurar.
`.env`, `.venv` y `data/` están excluidos de Git.

## 4. Crear o actualizar las tablas

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

La primera ejecución crea `institution`, `education` y `alembic_version`.
En ejecuciones posteriores aplica solo las migraciones pendientes y conserva
los datos. FastAPI no crea ni modifica tablas al arrancar.

Puedes comprobar la revisión instalada con:

```powershell
.\.venv\Scripts\python.exe -m alembic current
```

La revisión inicial es `0001`. Si reutilizas una base con tablas creadas por otra
herramienta y sin historial Alembic, revisa primero su esquema antes de incorporarla
mediante `alembic stamp 0001`; ese comando registra la revisión sin crear tablas.

## 5. Levantar la API

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Mantén esa terminal abierta. Prueba en:

- Swagger: **http://127.0.0.1:8000/docs**
- Instituciones: **http://127.0.0.1:8000/api/v1/institutions**
- Educación: **http://127.0.0.1:8000/api/v1/educations**
- OpenAPI: http://127.0.0.1:8000/openapi.json

Un GET con respuesta `[]` y estado `200` significa que funciona y no hay registros
activos. Detén la API con `Ctrl+C`.

### Volver a levantarlo otro día

Desde la raíz del repositorio, ejecuta:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Los registros continúan en `data/portfolio.db`. No necesitas repetir la instalación
ni crear otra base. Si actualizaste el código, instala los requisitos actualizados
y ejecuta `alembic upgrade head` antes de iniciar.

## Probar los CRUD

En Swagger abre una operación, pulsa **Try it out**, completa sus datos y pulsa
**Execute**. Las respuestas usan nombres camelCase.

### Instituciones

| Método | Ruta | Operación |
| --- | --- | --- |
| POST | `/api/v1/institutions` | Crear. |
| GET | `/api/v1/institutions?offset=0&limit=20` | Listar activas. |
| GET | `/api/v1/institutions/{institution_id}` | Consultar por ID. |
| PUT | `/api/v1/institutions/{institution_id}` | Reemplazar datos editables enviando `version`. |
| DELETE | `/api/v1/institutions/{institution_id}?version=0` | Borrar lógicamente. |

Ejemplo de POST:

```json
{
  "institutionName": "Example University",
  "institutionNameEs": "Universidad de ejemplo",
  "institutionUrl": "https://example.edu"
}
```

El nombre es obligatorio, no puede estar vacío y admite hasta 255 caracteres.
El nombre en español es opcional, con el mismo límite. La URL es texto opcional
de hasta 2048 caracteres. La respuesta añade `institutionId`, `institutionDeleted`
y `version`.

### Educación

| Método | Ruta | Operación |
| --- | --- | --- |
| POST | `/api/v1/educations` | Crear asociando una institución activa. |
| GET | `/api/v1/educations?offset=0&limit=20` | Listar por posición e ID. |
| GET | `/api/v1/educations/{education_id}` | Consultar por ID. |
| PUT | `/api/v1/educations/{education_id}` | Reemplazar datos editables enviando `version`. |
| DELETE | `/api/v1/educations/{education_id}?version=0` | Borrar lógicamente. |

Crea una institución primero y usa el ID devuelto en `institutionId`:

```json
{
  "educationTitle": "Software Engineering",
  "educationTitleEs": "Ingeniería de software",
  "educationPlace": "Quito",
  "educationStart": "September 2020",
  "educationStartEs": "Septiembre 2020",
  "educationEnd": "Present",
  "educationEndEs": "Actualidad",
  "educationPosition": 1,
  "educationVisible": true,
  "institutionId": 1
}
```

El ID `1` es ilustrativo. Título, lugar, fin, posición e institución son obligatorios.
Los textos admiten hasta 255 caracteres. Inicio y fin son texto, no fechas.
La posición es un entero de 32 bits; la visibilidad es `true` por defecto.

Filtros disponibles:

```text
GET /api/v1/educations?institutionId=1
GET /api/v1/educations?visible=true
GET /api/v1/educations?institutionId=1&visible=false
```

Sin el filtro `visible`, se muestran registros visibles y ocultos. Ocultar un
registro no lo elimina. Crear o actualizar exige una institución activa.
El borrado lógico del padre no elimina en cascada las educaciones existentes.

### Versiones, borrado y errores

POST genera el ID y la versión inicial `0`; no acepta identidad, versión ni
estado de borrado enviados por el cliente. En PUT envía los campos editables
completos y agrega `"version": 0`, o la versión obtenida en tu última consulta.
La respuesta incrementa la versión. Los campos opcionales omitidos se reemplazan
por `null`, y la visibilidad omitida vuelve a `true`.

DELETE recibe la versión actual en la URL. Marca la fila como eliminada e
incrementa su versión; devuelve `204`. La fila queda almacenada pero deja de
aparecer en las consultas y no puede actualizarse por el CRUD.

- `404`: recurso inexistente/eliminado o institución relacionada no activa.
- `409`: versión obsoleta o conflicto con restricciones de persistencia.
- `422`: datos inválidos o versión requerida ausente.
- `503`: fallo técnico de almacenamiento.

Los listados aceptan `offset >= 0` y `limit` entre `1` y `100`.

## Datos y respaldo

Los datos locales no se suben a Git. Para llevarlos a otra máquina, detén la API,
copia `data/portfolio.db` a la misma ruta del otro equipo y levanta el proyecto.
Para empezar con una base independiente, elige otra ruta en `DB_URL` y ejecuta
`alembic upgrade head` sobre ese archivo nuevo.

## Pruebas y herramientas de desarrollo

Opcionalmente instala las herramientas de desarrollo:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Las pruebas usan archivos SQLite temporales y no cambian `data/portfolio.db`.
Cubren ambos CRUD, relaciones, concurrencia, persistencia tras reinicios,
transacciones, migraciones y fronteras arquitectónicas. Las rutas de las pruebas
reflejan las de `src`.

Para preparar una migración futura, cambia el modelo y genera una revisión:

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "Describe schema change"
```

Revisa la revisión antes de aplicar `upgrade head`. Autogenerate conserva tablas,
índices y restricciones ajenos a los modelos. Las migraciones no se ejecutan
automáticamente al iniciar la API.
