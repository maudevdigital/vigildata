# Planificacion de sprints - VigilData

## Resumen

El proyecto se organiza en tres sprints. La priorizacion se basa en el objetivo principal de la aplicacion: reportar incidentes ciudadanos, visualizarlos en un mapa y transformar esos reportes en informacion util.

Estado consultado en Taiga al 19/05/2026:

- Sprint 1: cerrado.
- Sprint 2: cerrado.
- Sprint 3: cerrado (todas las HU en Done, 15 tareas tecnicas cerradas con evidencia de commit).

## Sprint 1

| Campo | Valor |
|-------|-------|
| Fechas | 20/04/2026 - 28/04/2026 |
| Estado en Taiga | Cerrado |
| Objetivo | Implementar el flujo principal de reporte y visualizacion de incidentes. |

### Historias incluidas

1. HU-03: Reportar incidente con GPS.
2. HU-04: Ver mapa con incidentes.

### Justificacion de prioridad

Estas historias representan el nucleo del producto. Sin reporte y visualizacion de incidentes, la aplicacion no cumple su proposito principal.

## Sprint 2

| Campo | Valor |
|-------|-------|
| Fechas | 29/04/2026 - 05/05/2026 |
| Estado en Taiga | Cerrado |
| Objetivo | Incorporar autenticacion y filtros para mejorar el uso real de los reportes. |

### Historias incluidas

1. HU-01: Registro de usuario con email.
2. HU-02: Inicio de sesion con JWT.
3. HU-05: Filtrar incidentes por comuna y fecha.

### Justificacion de prioridad

La autenticacion sostiene la confiabilidad de los reportes y permite controlar quien puede crear incidentes. El filtrado mejora la utilidad del mapa, permitiendo consultar informacion por comuna y rango de fechas.

## Sprint 3

| Campo | Valor |
|-------|-------|
| Fechas | 06/05/2026 - 19/05/2026 (extendido una semana) |
| Estado en Taiga | Cerrado |
| Objetivo | Mejorar la calidad, confianza y lectura analitica de los datos. |
| Evidencia | Commits `8bdf725` (HU-06/07) y `102dd2f` via PR #7 (HU-08). |

### Historias incluidas

1. HU-06: Clasificar incidente por tipo y nivel de riesgo.
2. HU-07: Moderar incidentes reportados.
3. HU-08: Ver resumen de incidentes por comuna y tipo.

### Justificacion de prioridad

Una vez implementado el flujo principal, estas historias aumentan el valor de los datos. La clasificacion permite interpretar mejor los reportes, la moderacion mejora su confiabilidad y el resumen facilita la toma de decisiones.

## Roadmap completo

| Sprint | Historias | Estado en Taiga | Resultado esperado |
|--------|-----------|-----------------|--------------------|
| Sprint 1 | HU-03, HU-04 | Cerrado | Flujo base de reporte y mapa. |
| Sprint 2 | HU-01, HU-02, HU-05 | Cerrado | Autenticacion y consulta filtrada. |
| Sprint 3 | HU-06, HU-07, HU-08 | Cerrado | Datos mas confiables y analisis basico. |
