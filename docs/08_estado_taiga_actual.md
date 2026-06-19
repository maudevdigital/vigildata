# Estado actual de Taiga - VigilData

Fecha de consulta directa: 2026-06-19 (re-verificado vía API para Hito 3; consulta previa 03/05/2026)  
Proyecto Taiga: Ingenieria de software 1  
Slug: `maudevdigital-ingenieria-de-software-1`  
ID de proyecto: `1786600`  
Fuente: consulta autenticada a la API de Taiga, `https://api.taiga.io/api/v1`

## Descripcion del proyecto

Mapa colaborativo de seguridad ciudadana que permite a los habitantes de una comuna reportar incidentes en su entorno y visualizarlos en tiempo real sobre un mapa interactivo. La idea central es convertir el conocimiento del barrio en datos utiles, sin formularios complicados ni infraestructura pesada.

## Integrantes y roles en Taiga

| Integrante | Usuario Taiga | Rol |
|------------|---------------|-----|
| benjaosan | `benjaosan` | Front |
| Felipe Vergara R | `FelipeVR` | Scrum Master |
| lucasmaulenr | `maudevdigital` | Product Owner |
| Sebastian Lopez Cisternas | `SebaNG` | Back |

## Sprints

| Sprint | Fechas planificadas | Estado en Taiga | Historias | Puntos cerrados |
|--------|---------------------|-----------------|-----------|-----------------|
| Sprint 1 | 2026-04-20 - 2026-04-28 | Cerrado | 2 | 100.0/100.0 |
| Sprint 2 | 2026-04-29 - 2026-05-05 | Cerrado | 3 | 150.0/150.0 |
| Sprint 3 | 2026-05-06 - 2026-05-12 | Cerrado | 6 | Todas las HU en Done |

## Historias de usuario

| Ref. Taiga | Historia | Sprint | Estado | Asignado | Cerrada |
|------------|----------|--------|--------|----------|---------|
| #1 | HU-01: Registro de usuario con email | Sprint 2 | Done | benjaosan | Si |
| #2 | HU-02: Inicio de sesion con JWT | Sprint 2 | Done | Sebastian Lopez Cisternas | Si |
| #3 | HU-03: Reportar incidente con GPS | Sprint 1 | Done | Sebastian Lopez Cisternas | Si |
| #4 | HU-04: Ver mapa con incidentes | Sprint 1 | Done | benjaosan | Si |
| #5 | HU-05: Filtrar incidentes por comuna y fecha | Sprint 2 | Done | Sebastian Lopez Cisternas | Si |
| #16 | HU-06: Clasificar incidente por tipo y nivel de riesgo | Sprint 3 | Done | Sebastian Lopez Cisternas | Si |
| #17 | HU-07: Moderar incidentes reportados | Sprint 3 | Done | Sebastian Lopez Cisternas | Si |
| #18 | HU-08: Ver resumen de incidentes por comuna y tipo | Sprint 3 | Done | benjaosan | Si |
| #54 | HU-09: Control de repeticion de denuncias con BERT | Sprint 3 | Done | maudevdigital | Si |
| #61 | HU-10: Autenticacion con Google | Sprint 3 | Done | maudevdigital | Si |
| #67 | HU-11: Mejorar interfaz movil (Reportar, Mapa, Admin) | Sprint 3 | Done | maudevdigital | Si |

## Tareas tecnicas registradas

### Sprint 1

| Ref. Taiga | Tarea | Historia asociada | Estado | Asignado |
|------------|-------|-------------------|--------|----------|
| #6 | [Front] Crear formulario de reporte de incidente | HU-03 | Closed | Sebastian Lopez Cisternas |
| #7 | [Front] Integrar Geolocation API | HU-03 | Closed | Sebastian Lopez Cisternas |
| #8 | [Back] Definir modelo de incidente | HU-03 | Closed | Sebastian Lopez Cisternas |
| #9 | [Back] Crear endpoint para registrar incidente | HU-03 | Closed | Sebastian Lopez Cisternas |
| #10 | [Back] Validar token y registrar fecha/hora | HU-03 | Closed | Sebastian Lopez Cisternas |
| #11 | [Front] Crear vista de mapa con Leaflet | HU-04 | Closed | benjaosan |
| #12 | [Front] Renderizar marcadores y popup informativo | HU-04 | Closed | benjaosan |
| #13 | [Front] Crear endpoint para listar incidentes | HU-04 | Closed | benjaosan |
| #15 | Crear marcadores interactivos en el mapa mediante GPS | HU-04 | Closed | benjaosan |

### Sprint 2

| Ref. Taiga | Tarea | Historia asociada | Estado | Asignado |
|------------|-------|-------------------|--------|----------|
| #19 | [Front] Crear vista de registro de usuario | HU-01 | Closed | benjaosan |
| #20 | [Front] Validar formulario de registro y mensajes de error | HU-01 | Closed | benjaosan |
| #21 | [Back] Crear endpoint POST /auth/registro | HU-01 | Closed | benjaosan |
| #22 | [Back] Validar email unico y hash de contrasena | HU-01 | Closed | benjaosan |
| #25 | [Front] Crear vista de inicio de sesion | HU-02 | Closed | Sebastian Lopez Cisternas |
| #26 | [Front] Persistir token y proteger navegacion | HU-02 | Closed | Sebastian Lopez Cisternas |
| #27 | [Back] Crear endpoint POST /auth/login y emitir JWT | HU-02 | Closed | Sebastian Lopez Cisternas |
| #28 | [Back] Validar token en endpoints protegidos | HU-02 | Closed | Sebastian Lopez Cisternas |
| #31 | [Front] Crear controles de filtro por comuna y fecha | HU-05 | Closed | benjaosan |
| #32 | [Front] Actualizar mapa/listado segun filtros | HU-05 | Closed | benjaosan |
| #33 | [Back] Implementar filtros comuna, fecha_inicio y fecha_fin | HU-05 | Closed | Sebastian Lopez Cisternas |
| #34 | [Back] Validar combinacion de filtros y formato de fechas | HU-05 | Closed | Sebastian Lopez Cisternas |

## Tareas tecnicas (resumen Hito 3)

Al 2026-06-19: **30 tareas tecnicas registradas, todas en estado Closed.**

## Issues

No hay issues registrados en Taiga (0 issues al 2026-06-19).

## Observaciones (estado final Hito 3)

- Los tres sprints (1, 2 y 3) aparecen **cerrados** en Taiga.
- Las 11 historias HU-01 a HU-11 estan en estado **Done** y cerradas.
- Sprint 3 quedo cerrado con las 6 historias HU-06 a HU-11 en Done.
- Las 30 tareas tecnicas estan cerradas y no existen issues abiertos.
- El tablero de Taiga esta **alineado con el codigo entregado**.
- El guion del Product Owner debe presentar Sprint 1 y Sprint 2 como incrementos cerrados hasta la consulta directa del 03/05/2026.
- Las tecnicas de prueba acordadas para el video son caja negra, aceptacion y unitarias.
- Las pruebas las ejecuta o demuestra el Scrum Team/developers; el Product Owner valida contra criterios de aceptacion.
- Sebastian Lopez Cisternas figura en Taiga como Back y con tareas asociadas, pero no se considera como expositor porque falto a la grabacion; se menciona solo por trazabilidad.
