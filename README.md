# CRUD de instituciones con FastAPI

API para la tabla PostgreSQL `institution`, con Python **3.14.7**, borrado lógico
y control optimista de versiones. La arquitectura reproduce la separación de
capas y puertos del proyecto Spring Boot examinado en
`HUS/src/main/java/com/pichincha/cigmsaspkagj`.

El análisis de esa referencia está en [ARCHITECTURE.md](ARCHITECTURE.md).
El código y los mensajes de la API están en inglés; los comentarios explicativos
y esta documentación están en español.

## Organización del código y las pruebas

`src/` es el paquete raíz de la aplicación. La funcionalidad de instituciones
se agrupa en `src/institution/`, con sus propias capas hexagonales. Sus pruebas
reflejan las mismas rutas bajo `tests/institution/`:

```text
src/
  main.py
  institution/
    domain/model/institution.py
    application/service/institution_service_impl.py
    application/port/input/institution_service.py
    application/port/output/institution_persistence_port.py
    infrastructure/config/settings.py
    infrastructure/input/adapter/rest/institution_controller.py
    infrastructure/output/adapter/repository/institution_persistence_adapter.py

tests/
  conftest.py
  architecture/test_architecture.py
  institution/
    domain/model/test_institution.py
    application/service/test_institution_service_impl.py
    infrastructure/config/test_settings.py
    infrastructure/input/adapter/rest/test_institution_controller.py
    infrastructure/input/adapter/rest/test_exception_handlers.py
    infrastructure/output/adapter/repository/test_institution_persistence_adapter.py
```

Las verificaciones que afectan a todas las capas están en `tests/architecture/`.
Las fixtures compartidas permanecen en `tests/conftest.py`. No hace falta crear
una prueba vacía por cada `__init__.py` o interfaz.
`src/main.py` mantiene el arranque general y registra los componentes de la funcionalidad.

## Preparar el entorno

Desde la raíz del repositorio:

```powershell
py -3.14 --version
py -3.14 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Comprueba que el intérprete muestre `Python 3.14.7`. Si `.venv` ya existe con esa
versión, puedes ejecutar directamente el comando de instalación.

La configuración se lee de las variables de entorno o del archivo `.env` de la
carpeta actual. Las variables del sistema tienen prioridad sobre `.env`.
En una copia nueva del repositorio, crea el archivo a partir del ejemplo:

```powershell
Copy-Item .env.example .env
```

Edita `.env` con tus valores locales:

```dotenv
DB_URL=jdbc:postgresql://localhost:5432/portfolio_db
DB_USERNAME=postgres
DB_PASSWORD=your-local-password
DB_DRIVER=org.postgresql.Driver
```

En este equipo ya se creó `.env` con los valores proporcionados. No se sube a Git.
La aplicación admite la URL JDBC para conservar los nombres de configuración,
pero la convierte a una URL `postgresql+psycopg` para Python. No utiliza el driver Java.

## Levantar la API

```powershell
.\.venv\Scripts\python.exe -m uvicorn src.main:app --reload
```

- Documentación interactiva: <http://127.0.0.1:8000/docs>
- Esquema OpenAPI: <http://127.0.0.1:8000/openapi.json>
- Documentación alternativa: <http://127.0.0.1:8000/redoc>

Mantén abierta la terminal mientras usas la API. Detén el servidor con `Ctrl+C`.
Ejecuta el comando desde la raíz del repositorio para que Python encuentre `src`.
La documentación puede abrirse sin conexión a PostgreSQL; las operaciones CRUD sí
requieren que la base de datos esté disponible.

## Endpoints

| Método | Ruta | Resultado |
| --- | --- | --- |
| POST | `/api/v1/institutions` | Crea una institución y devuelve `201`, ID y versión inicial `0`. |
| GET | `/api/v1/institutions?offset=0&limit=20` | Lista únicamente instituciones activas. |
| GET | `/api/v1/institutions/{institution_id}` | Consulta una institución activa. |
| PUT | `/api/v1/institutions/{institution_id}` | Reemplaza los datos editables y compara la versión enviada. |
| DELETE | `/api/v1/institutions/{institution_id}?version=0` | Marca la institución como eliminada e incrementa su versión; devuelve `204`. |

La paginación admite `offset >= 0` y `limit` entre `1` y `100`. Los identificadores
deben ser positivos.

### Crear

En Swagger selecciona `POST`, pulsa **Try it out** y envía:

```json
{
  "institutionName": "Example University",
  "institutionNameEs": "Universidad de ejemplo",
  "institutionUrl": "https://example.edu"
}
```

Respuesta de ejemplo:

```json
{
  "institutionId": 1,
  "institutionName": "Example University",
  "institutionNameEs": "Universidad de ejemplo",
  "institutionUrl": "https://example.edu",
  "institutionDeleted": false,
  "version": 0
}
```

El ID del ejemplo es ilustrativo. La API genera el ID y no permite enviar
`institutionId`, `institutionDeleted` ni `version` durante la creación.

### Actualizar

Consulta primero la institución y envía su versión actual en el cuerpo de `PUT`:

```json
{
  "institutionName": "Updated University",
  "institutionNameEs": null,
  "institutionUrl": "https://example.edu",
  "version": 0
}
```

La respuesta tendrá `version: 1`. PUT reemplaza los campos editables: los campos
opcionales omitidos quedan en `null`. El nombre es obligatorio, no puede estar
vacío y admite hasta 255 caracteres; el nombre en español es opcional con el mismo
límite; la URL es texto opcional de hasta 2048 caracteres, igual que en la entidad Java.

### Eliminar

Si la versión actual es `1`, usa:

```text
DELETE /api/v1/institutions/1?version=1
```

No se ejecuta un DELETE físico. La fila permanece con `institution_deleted=true`
y `version=2`. Después deja de aparecer en GET y no se puede actualizar por esta API.

### Respuestas de error

- `404`: institución inexistente o eliminada.
- `409`: versión obsoleta o conflicto con una restricción de base de datos.
- `422`: solicitud inválida, campos no permitidos o versión requerida ausente.
- `503`: fallo técnico de persistencia; no se exponen detalles SQL ni credenciales.

Ante un `409` de versión, vuelve a consultar el registro antes de decidir si
reenvías tu cambio. Tanto PUT como DELETE comparan e incrementan la versión dentro
de una misma sentencia SQL para evitar actualizaciones perdidas.

## Base de datos

La aplicación usa la tabla existente y **no crea ni altera tablas al arrancar**.
Se confirmó que la tabla local tiene estas columnas:

```text
institution_id       BIGINT, clave primaria autogenerada
institution_name     VARCHAR(255), obligatorio
institution_name_es  VARCHAR(255), opcional
institution_url      VARCHAR(2048), opcional
institution_deleted  BOOLEAN, obligatorio
version              BIGINT, obligatorio
```

Para una base nueva, [database/schema.sql](database/schema.sql) contiene el esquema
de referencia. Su ejecución es manual; no hace falta aplicarlo a la tabla existente.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m ruff format --check .
```

Por defecto se utiliza SQLite temporal para las pruebas del CRUD. Para verificar
también el mismo flujo en PostgreSQL:

```powershell
$env:RUN_POSTGRES_TESTS = "1"
.\.venv\Scripts\python.exe -m pytest
Remove-Item Env:RUN_POSTGRES_TESTS
```

Cada prueba PostgreSQL crea un esquema con nombre aleatorio y lo elimina al terminar.
Se requiere permiso para crear esquemas. Las pruebas no escriben en `public.institution`.
Se verifican CRUD, validaciones, filas eliminadas, concurrencia, errores técnicos y
fronteras arquitectónicas.
