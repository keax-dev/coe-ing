# Arquitectura de componentes backend

## Referencia analizada

Se examinó únicamente la organización arquitectónica de
`C:/Users/jimen/Documents/HUS/src/main/java/com/pichincha/cigmsaspkagj`, junto con
sus convenciones de arquitectura en `HUS/AGENTS.md`. No se modificó el proyecto Java
ni se trasladó su lógica de reservas, clientes o inventario.

La referencia tiene una estructura hexagonal de puertos y adaptadores:

- `domain/model` contiene modelos de negocio sin anotaciones de persistencia.
- `domain/exception` representa fallos sin depender de estados HTTP.
- `application/port/input` define contratos de casos de uso.
- `application/port/output` define contratos de persistencia y servicios externos.
- `application/service` implementa puertos de entrada mediante puertos de salida.
- `infrastructure/output/adapter/repository` implementa persistencia, separando
  `entity`, `repository` y `mapper`.
- `infrastructure/output/adapter/rest/client` contiene integraciones HTTP salientes.
- `infrastructure/config/ApplicationConfiguration` ensambla servicios y puertos.

En la carpeta Java examinada no se encontró un controlador de entrada REST.
Sus convenciones indican que debe ubicarse en `infrastructure/input/adapter/rest`;
esta implementación añade ahí el adaptador REST que requiere el CRUD en FastAPI.
Los clientes externos de la referencia no se reproducen porque este CRUD no los necesita.

## Correspondencia en Python

```text
institution/
    main.py
    domain/
        model/institution.py
        exception/institution_errors.py
    application/
        port/input/institution_service.py
        port/output/institution_persistence_port.py
        service/institution_service_impl.py
    infrastructure/
        config/
            settings.py
            database_configuration.py
            application_configuration.py
        input/adapter/rest/
            institution_controller.py
            exception_handlers.py
            dto/institution_dto.py
            mapper/institution_rest_mapper.py
        output/adapter/repository/
            institution_persistence_adapter.py
            entity/institution_entity.py
            repository/institution_repository.py
            mapper/institution_persistence_mapper.py
```

`Protocol` expresa los contratos de aplicación. Los servicios implementan el puerto
de entrada y reciben el puerto de salida por constructor, igual que las interfaces
y la inyección por constructor de la referencia.

## Recorrido de una solicitud

```text
HTTP JSON
  -> DTO Pydantic validado
  -> Mapper REST
  -> Puerto de entrada InstitutionService
  -> InstitutionServiceImpl
  -> Puerto de salida InstitutionPersistencePort
  -> InstitutionPersistenceAdapter
  -> InstitutionRepository + SQLAlchemy
  -> PostgreSQL
```

La respuesta recorre los mappers en sentido inverso. Los DTO y entidades ORM nunca
se intercambian a través de los puertos: estos solo utilizan modelos de dominio
y tipos estándar de Python.

## Reglas de dependencia

- Dominio no importa aplicación, infraestructura, FastAPI, Pydantic ni SQLAlchemy.
- Aplicación no importa infraestructura, HTTP ni ORM.
- El controlador depende del puerto de entrada, no del servicio concreto ni del repositorio.
- El adaptador de salida implementa el puerto de salida y no importa adaptadores de entrada.
- Los mappers REST y de persistencia son independientes y convierten explícitamente sus modelos.
- La configuración de infraestructura es el punto que conoce las implementaciones y las ensambla.
- Las pruebas de arquitectura comprueban estas fronteras y la ausencia de ciclos de importación.

## Equivalencia con la entidad proporcionada

| Spring/Hibernate | Implementación FastAPI |
| --- | --- |
| `@Entity`, `@Table`, `@Column` | `InstitutionEntity` con SQLAlchemy, separado del dominio. |
| `GenerationType.IDENTITY` | Columna BIGINT autogenerada por PostgreSQL. |
| `@SQLRestriction` | Predicado `institution_deleted=false` en todas las consultas públicas y escrituras. |
| `@Version` | Predicado por versión e incremento atómico en cada PUT y borrado lógico. |
| `@SQLDelete` | UPDATE que marca la fila como eliminada e incrementa la versión. |
| Verificación de fila afectada | RETURNING distingue una escritura exitosa de un registro ausente o una versión obsoleta. |

La versión inicial es `0`. El cliente debe enviar la versión observada para cambiar
o eliminar un registro; las discrepancias se expresan como un error de dominio y
el adaptador REST las traduce a `409`.

Cada operación del adaptador de persistencia dispone de su propia sesión y
transacción. Los modelos se convierten antes de cerrar la sesión y la confirmación
termina antes de responder éxito. Los fallos técnicos se traducen a errores del
dominio sin filtrar SQL ni credenciales al consumidor.
