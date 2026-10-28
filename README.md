# CRUD de instituciones y educación con FastAPI

Dos funcionalidades con arquitecturas distintas en una API compatible con
**Python 3.14.7**:

- `src/institution/hexagonal`: instituciones con puertos y adaptadores.
- `src/education/clean`: educación con dominio, aplicación, infraestructura y presentación.

Ambas usan PostgreSQL, borrado lógico y control optimista de versiones.
Los detalles de las capas están en [ARCHITECTURE.md](ARCHITECTURE.md).
Los comentarios y la documentación están en español; los identificadores y los
mensajes de la API están en inglés.

## Instalación y arranque

Desde la raíz del repositorio:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Comprueba que el intérprete muestre `Python 3.14.7`. Si el entorno ya existe con
esa versión, puedes omitir su creación. En una copia nueva del repositorio,
prepara las variables locales:

```powershell
Copy-Item .env.example .env
```

Edita `.env` con tus credenciales. En este equipo ya está configurado con los
valores proporcionados. Se conserva la configuración original:

```dotenv
DB_URL=jdbc:postgresql://localhost:5432/portfolio_db
DB_USERNAME=postgres
DB_PASSWORD=your-local-password
DB_DRIVER=org.postgresql.Driver
```

Las variables del sistema tienen prioridad sobre `.env`. La URL JDBC se adapta
a `postgresql+psycopg`; no se necesita el driver Java. `.env` está excluido de Git.

Levanta PostgreSQL y después ejecuta:

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

Abre **http://127.0.0.1:8000/docs** para probar ambos CRUD. También están disponibles
`/redoc` y `/openapi.json`. Mantén la terminal abierta y usa `Ctrl+C` para detener
el servidor. La documentación puede abrirse sin conexión a PostgreSQL; los CRUD
requieren una conexión válida.

## Estructura

```text
src/
  main.py
  institution/
    hexagonal/
      domain/
      application/
      infrastructure/
  education/
    clean/
      domain/
        model/education.py
        exception/education_errors.py
      application/
        port/education_repository.py
        port/institution_lookup.py
        port/unit_of_work.py
        service/education_service.py
      infrastructure/
        model/education_model.py
        mapper/education_persistence_mapper.py
        repository/education_repository.py
        gateway/institution_lookup.py
        unit_of_work/sqlalchemy_unit_of_work.py
      presentation/
        schema/education_schema.py
        mapper/education_rest_mapper.py
        dependency/education_dependencies.py
        exception/education_exception_handlers.py
        router/education_router.py
  shared/
    config/
    persistence/

tests/
  conftest.py
  architecture/
  institution/hexagonal/...
  education/clean/...
  shared/...

migrations/
  env.py
  script.py.mako
  versions/0001_initial_schema.py

alembic.ini
```

Las pruebas de cada componente reflejan su ruta en `src`. Las fixtures comunes
quedan en `tests/conftest.py`; las reglas entre capas, en `tests/architecture/`.
La configuración de conexión y los metadatos SQL compartidos son detalles técnicos,
no modelos de negocio compartidos entre las dos funcionalidades.

Cada componente tiene su carpeta y su archivo Python. Por ejemplo,
`src/education/clean/domain/model/education.py` tiene su prueba en
`tests/education/clean/domain/model/test_education.py`. Las pruebas del servicio,
repositorio, unidad de trabajo, esquemas y rutas siguen la misma correspondencia.

En educación, el servicio abre una unidad de trabajo por operación. La consulta de
la institución y las escrituras comparten sesión y transacción; los repositorios
no hacen commit. El caso de uso confirma cuando termina correctamente y, si hay
un error o falta la confirmación, se revierte la transacción.

## Instituciones: arquitectura hexagonal

Base: **http://127.0.0.1:8000/api/v1/institutions**

| Método | Ruta | Operación |
| --- | --- | --- |
| POST | `/api/v1/institutions` | Crear; responde `201` con versión inicial `0`. |
| GET | `/api/v1/institutions?offset=0&limit=20` | Listar activas. |
| GET | `/api/v1/institutions/{institution_id}` | Consultar una activa. |
| PUT | `/api/v1/institutions/{institution_id}` | Reemplazar datos editables enviando `version`. |
| DELETE | `/api/v1/institutions/{institution_id}?version=0` | Borrado lógico; responde `204`. |

Ejemplo de creación:

```json
{
  "institutionName": "Example University",
  "institutionNameEs": "Universidad de ejemplo",
  "institutionUrl": "https://example.edu"
}
```

El nombre es obligatorio y admite hasta 255 caracteres; el nombre en español es
opcional, con el mismo límite. La URL es texto opcional de hasta 2048 caracteres.
La respuesta incluye `institutionId`, `institutionDeleted` y `version`.

## Educación: Clean Architecture

Base: **http://127.0.0.1:8000/api/v1/educations**

| Método | Ruta | Operación |
| --- | --- | --- |
| POST | `/api/v1/educations` | Crear asociando una institución activa. |
| GET | `/api/v1/educations?offset=0&limit=20` | Listar registros no eliminados, por posición e ID. |
| GET | `/api/v1/educations/{education_id}` | Consultar uno no eliminado. |
| PUT | `/api/v1/educations/{education_id}` | Reemplazar datos editables enviando `version`. |
| DELETE | `/api/v1/educations/{education_id}?version=0` | Borrado lógico; responde `204`. |

Crea una institución primero y utiliza el ID devuelto; `1` es solo ilustrativo:

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

Título, lugar, fin, posición e institución son obligatorios. Todos los campos de
texto admiten hasta 255 caracteres. Inicio y fin se mantienen como **texto**, igual
que los `String` de Java: no se convierten en fechas. La posición admite el rango
de un `int` de Java, incluidos valores negativos. La visibilidad es `true` por defecto.
La respuesta añade `educationId`, `educationDeleted` y `version`.

Puedes filtrar el listado:

```text
GET /api/v1/educations?institutionId=1
GET /api/v1/educations?visible=true
GET /api/v1/educations?institutionId=1&visible=false&offset=0&limit=20
```

Sin `visible`, se devuelven tanto registros visibles como ocultos. Ocultar un
registro no lo elimina. Crear o actualizar requiere una institución activa; un ID
inexistente o eliminado devuelve `404`.

El borrado lógico de una institución no elimina en cascada las educaciones ya
registradas. Se conserva su relación histórica y pueden consultarse o eliminarse.
Para actualizarlas debes asociarlas a una institución activa.

## Versiones, actualizaciones y errores

Los dos CRUD generan ID, estado de borrado y versión inicial `0` en el servidor.
Estos campos no se aceptan en POST. Para PUT, envía los campos editables completos
y agrega la versión obtenida en la última consulta:

```json
{
  "educationTitle": "Updated degree",
  "educationPlace": "Quito",
  "educationEnd": "Present",
  "educationPosition": 1,
  "educationVisible": false,
  "institutionId": 1,
  "version": 0
}
```

La respuesta tendrá `version: 1`. Los campos opcionales omitidos quedan en `null`;
la visibilidad omitida vuelve a `true`. En instituciones, PUT sigue el mismo
contrato de reemplazo de sus datos editables.

Para eliminar, envía la versión actual en la URL. Si es `1`:

```text
DELETE /api/v1/educations/1?version=1
```

La fila queda con `education_deleted=true` y `version=2`; deja de aparecer en GET
y no puede actualizarse por la API. El ID es ilustrativo.

- `404`: registro inexistente/eliminado o institución relacionada no activa.
- `409`: versión obsoleta o conflicto con una restricción de persistencia.
- `422`: datos inválidos, campos no permitidos o versión requerida ausente.
- `503`: fallo técnico de persistencia, sin exponer SQL ni credenciales.

Ante un conflicto de versión, consulta el registro antes de decidir si reenvías
el cambio. La comparación y el incremento de versión ocurren en una misma
sentencia SQL. Ambos listados admiten `offset >= 0` y `limit` entre `1` y `100`.

## Base de datos y pruebas

La aplicación **no crea ni altera tablas al arrancar**. Se confirmó que las tablas
locales `institution` y `education` coinciden con las entidades proporcionadas,
incluida la clave foránea `education.institution_id`.
[database/schema.sql](database/schema.sql) es una referencia manual para una base nueva.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Las pruebas de integración utilizan SQLite temporal por defecto, con las claves
foráneas habilitadas. Para ejecutar también el mismo flujo en PostgreSQL:

```powershell
$env:RUN_POSTGRES_TESTS = "1"
.\.venv\Scripts\python.exe -m pytest
Remove-Item Env:RUN_POSTGRES_TESTS
```

Cada prueba PostgreSQL crea un esquema aleatorio y lo elimina al terminar. Se
requiere permiso para crear esquemas; las pruebas no escriben en las tablas
públicas existentes. Se verifican ambos CRUD, relaciones, filtros, concurrencia,
validación, persistencia y fronteras arquitectónicas.

## Migraciones con Alembic

Alembic está incluido en `requirements.txt`. Si tu entorno ya estaba instalado,
actualízalo con `python -m pip install -r requirements.txt` usando el intérprete
de `.venv` mostrado arriba.

La revisión `0001` crea las tablas de referencia en una **base nueva**:

```powershell
.\.venv\Scripts\python.exe -m alembic upgrade head
```

En tu base actual las tablas ya existen: no se debe ejecutar esa creación inicial
sobre ellas. Después de revisar la correspondencia del esquema, puedes registrar
la línea base sin recrear las tablas y comprobar diferencias:

```powershell
.\.venv\Scripts\python.exe -m alembic stamp 0001
.\.venv\Scripts\python.exe -m alembic check
```

`stamp` registra la revisión en `alembic_version`; no aplica el DDL de `0001`.
El proyecto no ejecuta estos comandos automáticamente. Durante la implementación
solo se probaron migraciones en bases temporales y esquemas PostgreSQL aislados.

La configuración de autogeneración se limita a las tablas de ambas funcionalidades
y conserva índices y restricciones existentes que no estén declarados en los
modelos. Se detectaron índices adicionales en la base actual: no se eliminan ni
se incluyen automáticamente en la revisión mínima para bases nuevas.

Para preparar una modificación futura del esquema:

```powershell
.\.venv\Scripts\python.exe -m alembic revision --autogenerate -m "Describe schema change"
```

Revisa el archivo generado antes de aplicar `upgrade head`. La revisión inicial
también tiene un `downgrade` que elimina sus tablas; no es un comando de arranque.
Las pruebas de migraciones están en `tests/migrations/` y comprueban creación,
reversión y adopción de tablas existentes sin pérdida de registros ni índices.
