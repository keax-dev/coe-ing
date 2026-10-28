# Arquitecturas por funcionalidad

Instituciones conserva una arquitectura hexagonal y educación implementa Clean
Architecture con capas de dominio, aplicación, infraestructura y presentación.
El punto de arranque compartido continúa siendo `src.main:app`.

```text
src/
  main.py
  institution/hexagonal/
    domain/
    application/
    infrastructure/
  education/clean/
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
```

## Instituciones: arquitectura hexagonal

La referencia es la organización de
`C:/Users/jimen/Documents/HUS/src/main/java/com/pichincha/cigmsaspkagj` y sus
convenciones en `HUS/AGENTS.md`. El proyecto Java no se modificó.

- `domain`: modelos y errores independientes de HTTP y ORM.
- `application/port/input`: contratos de casos de uso.
- `application/port/output`: contratos de persistencia.
- `application/service`: implementación mediante puertos de salida.
- `infrastructure/input/adapter/rest`: controladores, DTO, mappers y respuestas de error.
- `infrastructure/output/adapter/repository`: adaptador, repositorio, entidad SQL y mapper.
- `infrastructure/config`: ensamblado por constructor.

```text
HTTP -> Puerto de entrada -> Servicio -> Puerto de salida -> Adaptador -> PostgreSQL
```

## Educación: Clean Architecture

Las dependencias apuntan al dominio y a los contratos de aplicación:

| Capa | Responsabilidad | Dependencias |
| --- | --- | --- |
| `domain` | Entidad `Education` y sus reglas de negocio. | Biblioteca estándar y su propia capa. |
| `application` | Casos de uso y contratos de repositorio, consulta institucional y unidad de trabajo. | Dominio y su propia capa. |
| `infrastructure` | Modelos SQLAlchemy, repositorios, gateway y transacciones. | Contratos internos, dominio y herramientas externas. |
| `presentation` | Validación HTTP, serialización, rutas, errores y ensamblado. | Aplicación, dominio y FastAPI/Pydantic. |

Solo `presentation/dependency` conoce infraestructura para ensamblar las
implementaciones. Los routers no importan repositorios concretos ni SQLAlchemy.
Dominio y aplicación no importan infraestructura, presentación ni frameworks.

```text
HTTP
  -> presentation/router/education_router.py
  -> presentation/schema + presentation/mapper
  -> application/service/education_service.py
  -> application/port/UnitOfWork
  -> infrastructure/unit_of_work/SQLAlchemyUnitOfWork
  -> infrastructure/repository + infrastructure/gateway
  -> PostgreSQL

Resultado: Education -> EducationRestMapper -> EducationResponse -> HTTP JSON
```

El servicio devuelve entidades de dominio. Ya no hay un controlador y presentador
intermedios ni DTO de dataclass duplicados: los esquemas HTTP están en presentación
y el mapper realiza la conversión explícita.

## Unidad de trabajo

`EducationService` recibe una fábrica del contrato `UnitOfWork`. Cada operación
crea una instancia, que abre su sesión y proporciona:

- `educations`: contrato del repositorio de educación.
- `institutions`: contrato de consulta de instituciones.
- `commit()` y `rollback()`: control explícito de la transacción.

Al crear o actualizar, el servicio valida la institución mediante la misma unidad
de trabajo que escribirá educación. El gateway puede bloquear la fila con
`SELECT FOR UPDATE`; el bloqueo se mantiene hasta confirmar o revertir.

Los repositorios realizan consultas, actualizaciones y `flush`, pero nunca
confirman ni abren transacciones independientes. El servicio hace commit cuando
la operación completa termina correctamente. Salir sin commit descarta las
escrituras; salir con un error provoca rollback y siempre cierra la sesión.
Las lecturas también cierran su transacción sin hacer commit.

La implementación externa traduce restricciones SQL a conflictos de persistencia
y otros errores SQLAlchemy a indisponibilidad. El servicio no recibe errores
propios del driver. La presentación decide los estados HTTP y no filtra SQL ni
credenciales.

## Relación institucional y versiones

`Education` contiene `institution_id`, no una entidad de otra funcionalidad.
El gateway consulta las columnas necesarias sin importar la implementación
hexagonal. Los metadatos SQL se comparten únicamente para resolver la clave
foránea entre tablas.

Crear o actualizar una educación requiere una institución activa. El borrado
lógico de una institución no elimina las educaciones previas: se conserva la
relación histórica. Para cambiarlas hay que elegir una institución activa.

En ambos CRUD, la versión inicial es `0`. PUT compara la versión e incrementa el
contador con un UPDATE atómico. DELETE realiza un UPDATE lógico que también
incrementa la versión. Las consultas omiten registros eliminados; la visibilidad
de educación es un atributo distinto del borrado.

## Pruebas reflejadas y migraciones

Los archivos de `tests/education/clean` tienen las mismas capas y carpetas que
`src/education/clean`. El nombre agrega `test_`, por ejemplo:

```text
src/education/clean/infrastructure/unit_of_work/sqlalchemy_unit_of_work.py
tests/education/clean/infrastructure/unit_of_work/test_sqlalchemy_unit_of_work.py
```

Las fixtures comunes permanecen en `tests/conftest.py`. Las reglas transversales
están en `tests/architecture/`. Se comprueban la dirección de dependencias, la
ausencia de ciclos, las rutas reflejadas y que los repositorios no hagan commit.
Las pruebas de integración usan SQLite temporal y PostgreSQL en esquemas aislados.

`migrations/env.py` registra los modelos de ambas funcionalidades y utiliza las
mismas variables de entorno. La revisión `0001` crea el esquema mínimo para bases
nuevas. Una base existente se incorpora mediante un stamp explícito después de
revisar su correspondencia. La API no aplica migraciones al arrancar.

Autogenerate excluye tablas ajenas y no propone eliminar índices o restricciones
existentes que no estén modelados. Los índices adicionales de la base de trabajo
se conservan; no se trasladan automáticamente al esquema mínimo de una base nueva.
Las pruebas de `tests/migrations/` verifican upgrade, downgrade y stamp en bases
aisladas, conservando registros e índices existentes.
