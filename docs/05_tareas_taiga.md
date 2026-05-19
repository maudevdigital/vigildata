# Tareas tecnicas registradas en Taiga

## Contexto

Las tareas tecnicas fueron consultadas directamente desde Taiga para el proyecto `Ingenieria de software 1`. Su objetivo es reflejar el trabajo real del Scrum Team y facilitar el seguimiento durante daily/reviews.

Estado general (al 19/05/2026):

- Sprint 1 aparece cerrado en Taiga.
- Sprint 2 aparece cerrado en Taiga.
- Sprint 3 aparece cerrado en Taiga (todas las HU en Done).
- Todas las tareas registradas para Sprint 1, Sprint 2 y Sprint 3 aparecen en estado `Closed`.
- No hay issues registrados al momento de la consulta directa.

## Sprint 1

### HU-03: Reportar incidente con GPS

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #6 | [Front] Crear formulario de reporte de incidente | Sebastian Lopez Cisternas | Closed |
| #7 | [Front] Integrar Geolocation API | Sebastian Lopez Cisternas | Closed |
| #8 | [Back] Definir modelo de incidente | Sebastian Lopez Cisternas | Closed |
| #9 | [Back] Crear endpoint para registrar incidente | Sebastian Lopez Cisternas | Closed |
| #10 | [Back] Validar token y registrar fecha/hora | Sebastian Lopez Cisternas | Closed |

### HU-04: Ver mapa con incidentes

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #11 | [Front] Crear vista de mapa con Leaflet | benjaosan | Closed |
| #12 | [Front] Renderizar marcadores y popup informativo | benjaosan | Closed |
| #13 | [Front] Crear endpoint para listar incidentes | benjaosan | Closed |
| #15 | Crear marcadores interactivos en el mapa mediante GPS | benjaosan | Closed |

## Sprint 2

### HU-01: Registro de usuario con email

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #19 | [Front] Crear vista de registro de usuario | benjaosan | Closed |
| #20 | [Front] Validar formulario de registro y mensajes de error | benjaosan | Closed |
| #21 | [Back] Crear endpoint POST /auth/registro | benjaosan | Closed |
| #22 | [Back] Validar email unico y hash de contrasena | benjaosan | Closed |

### HU-02: Inicio de sesion con JWT

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #25 | [Front] Crear vista de inicio de sesion | Sebastian Lopez Cisternas | Closed |
| #26 | [Front] Persistir token y proteger navegacion | Sebastian Lopez Cisternas | Closed |
| #27 | [Back] Crear endpoint POST /auth/login y emitir JWT | Sebastian Lopez Cisternas | Closed |
| #28 | [Back] Validar token en endpoints protegidos | Sebastian Lopez Cisternas | Closed |

### HU-05: Filtrar incidentes por comuna y fecha

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #31 | [Front] Crear controles de filtro por comuna y fecha | benjaosan | Closed |
| #32 | [Front] Actualizar mapa/listado segun filtros | benjaosan | Closed |
| #33 | [Back] Implementar filtros comuna, fecha_inicio y fecha_fin | Sebastian Lopez Cisternas | Closed |
| #34 | [Back] Validar combinacion de filtros y formato de fechas | Sebastian Lopez Cisternas | Closed |

## Sprint 3

Todas las tareas se crearon durante este sprint y se cerraron con evidencia de commit en el repositorio.

### HU-06: Clasificar incidente por tipo y nivel de riesgo

Commit principal: `8bdf725`.

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #37 | Backend: agregar enums TipoIncidente y NivelRiesgo en modelo | Sebastian Lopez Cisternas | Closed |
| #38 | Backend: validar tipo y nivel_riesgo en schemas y POST | Sebastian Lopez Cisternas | Closed |
| #39 | Backend: exponer tipo y nivel_riesgo en GET /incidentes | Sebastian Lopez Cisternas | Closed |
| #40 | Frontend: select de nivel_riesgo en ReportarView | Sebastian Lopez Cisternas | Closed |
| #41 | Frontend: colorear marcadores Leaflet por nivel_riesgo | Sebastian Lopez Cisternas | Closed |
| #42 | Frontend: leyenda de niveles de riesgo en MapaView | Sebastian Lopez Cisternas | Closed |

### HU-07: Moderar incidentes reportados

Commit principal: `8bdf725`.

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #44 | Backend: agregar estado, revisado_por_id, fecha_revision en modelo | Sebastian Lopez Cisternas | Closed |
| #46 | Backend: validacion de rol ANALISTA + endpoint PATCH /incidentes/{id}/estado | Sebastian Lopez Cisternas | Closed |
| #47 | Backend: GET / filtra solo aprobados + soporte ?estado=pendiente | Sebastian Lopez Cisternas | Closed |
| #48 | Frontend: acciones Aprobar/Rechazar/Eliminar en AdminView | Sebastian Lopez Cisternas | Closed |
| #49 | Frontend: enlace Moderacion visible solo a ANALISTA | Sebastian Lopez Cisternas | Closed |

### HU-08: Ver resumen de incidentes por comuna y tipo

Commit principal: `102dd2f` (PR #7).

| Ref. Taiga | Tarea | Responsable | Estado |
|------------|-------|-------------|--------|
| #50 | Backend: endpoint GET /incidentes/resumen | benjaosan | Closed |
| #51 | Frontend: componente IncidenteResumen.vue | benjaosan | Closed |
| #52 | Frontend: integrar filtros activos con endpoint resumen | benjaosan | Closed |
| #53 | Frontend: layout responsive del resumen | benjaosan | Closed |

## Pruebas acordadas

Para la explicacion del proyecto se usaran tres tecnicas:

1. Pruebas de caja negra.
2. Pruebas de aceptacion.
3. Pruebas unitarias.

La ejecucion de estas pruebas corresponde al Scrum Team/developers. El Product Owner valida la evidencia contra los criterios de aceptacion de cada historia.
