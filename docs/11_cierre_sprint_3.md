# Cierre Sprint 3 — VigilData

## Resumen ejecutivo

| Item | Valor |
|------|-------|
| Periodo | 06/05/2026 — 19/05/2026 |
| Estado | Cerrado (todas las HU en Done) |
| User stories cerradas | HU-06, HU-07, HU-08 |
| Tareas tecnicas cerradas | 15 (#37-#42, #44, #46-#53) |
| Pull requests mergeados | PR #7 (HU-08) |
| Cobertura de tests backend | 78.75% (sobre el minimo 60% del taller) |

## Evidencia por user story

### HU-06: Clasificar incidente por tipo y nivel de riesgo

- Modelo `Incidente` extendido con `nivel_riesgo`, `region`, `comuna` en `vigildata-backend/app/models/incidente.py`.
- `IncidenteCreate` e `IncidenteResponse` validan los nuevos campos.
- `ReportarView.vue` agrega selectores de tipo, nivel de riesgo y region/comuna en cascada.
- `MapaView.vue` colorea marcadores SVG por nivel (verde/amarillo/rojo).
- Commit principal: `8bdf725` "Actualizacion".

### HU-07: Moderar incidentes reportados

- Modelo agrega `estado` (pendiente/aprobado/rechazado), `revisado_por_id`, `fecha_revision`.
- `PATCH /incidentes/{id}/estado` valida rol ANALISTA inline.
- `DELETE /incidentes/{id}` solo para ANALISTA.
- `GET /incidentes` por defecto excluye `rechazado`; soporta `?estado=pendiente|aprobado|rechazado|todos`.
- `AdminView.vue` con tabs (pendientes/aprobados/rechazados) y botones Aprobar/Rechazar/Eliminar.
- Commit principal: `8bdf725`.

### HU-08: Ver resumen de incidentes por comuna y tipo

- Helper `_aplicar_filtros()` extraido para reuso entre listado y resumen.
- Endpoint `GET /incidentes/resumen` devuelve `{total, por_comuna, por_tipo}` con `func.count() + group_by`, reutilizando los mismos filtros del listado.
- Schemas `ConteoItem` e `IncidenteResumenResponse`.
- Componente `IncidenteResumen.vue` (panel colapsable) con barras CSS por comuna y tipo.
- `MapaView.vue` llama `/incidentes/resumen` en paralelo con el listado al aplicar filtros.
- Commit principal: `102dd2f` via PR #7.

## Validacion end-to-end (19/05/2026)

Probado con backend en SQLite local (Supabase fue eliminado) + frontend Vite dev:

| Test | Resultado |
|------|-----------|
| Registro + login ciudadano | OK rol CIUDADANO |
| Login admin seed `admin@vigildata.cl` / `admin123` | OK rol ANALISTA |
| Crear 4 incidentes (3 comunas, 3 niveles) | OK 201 |
| Moderar: 3 aprobados, 1 rechazado | OK 200 |
| `GET /incidentes/` esconde rechazados | OK devuelve 3 |
| `GET /incidentes/resumen` | OK totales correctos |
| `GET /incidentes/resumen?comuna=Santiago` | OK filtrado |
| `GET /incidentes/resumen?estado=todos` | OK incluye rechazados |
| Click en mapa abre modal de reporte (#97cd01e) | OK |
| Tras crear, mapa centra en el nuevo punto (#77c16c3) | OK |

## Fix tecnico aplicado durante la validacion

Commit `5882711`: agregar `foreign_keys="Incidente.usuario_id"` a la relacion `Usuario.incidentes` para resolver `AmbiguousForeignKeysError` introducido por la segunda FK (`revisado_por_id`). Esto tambien desbloquea los 5 tests que fallaban en `pytest`.

## Cambios en la documentacion

- README.md ahora documenta dos opciones de base de datos (SQLite local por defecto, Supabase opcional).
- `vigildata-backend/.env.example` con ambos perfiles configurados.
- `run.md` con seccion 0 de configuracion previa.
- `.gitignore` agrega `*.db` para no commitear la BD local.

## Pendiente para el Hito 2

1. Mergear cambios documentales finales (este commit).
2. Grabar el video demo de 3 minutos siguiendo el guion del documento `09_daily_meeting_3_video_pruebas.md`.
3. (Opcional, post-Hito 2) Aprovisionar un nuevo proyecto Supabase si se quiere produccion en la nube.
