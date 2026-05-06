# Planificación de sprints - VigilData

## Resumen

El proyecto se organiza en tres sprints. La priorización se basa en el objetivo principal de la aplicación: reportar incidentes ciudadanos, visualizarlos en un mapa y transformar esos reportes en información útil.

## Sprint 1

| Campo | Valor |
|-------|-------|
| Fechas | 20/04/2026 - 28/04/2026 |
| Objetivo | Implementar el flujo principal de reporte y visualización de incidentes. |

### Historias incluidas

1. HU-03: Reportar incidente con GPS.
2. HU-04: Ver mapa con incidentes.

### Justificación de prioridad

Estas historias representan el núcleo del producto. Sin reporte y visualización de incidentes, la aplicación no cumple su propósito principal.

## Sprint 2

| Campo | Valor |
|-------|-------|
| Fechas | 29/04/2026 - 05/05/2026 |
| Objetivo | Incorporar autenticación y filtros para mejorar el uso real de los reportes. |

### Historias incluidas

1. HU-01: Registro de usuario con email.
2. HU-02: Inicio de sesión con JWT.
3. HU-05: Filtrar incidentes por comuna y fecha.

### Justificación de prioridad

La autenticación sostiene la confiabilidad de los reportes y permite controlar quién puede crear incidentes. El filtrado mejora la utilidad del mapa, permitiendo consultar información por comuna y rango de fechas.

## Sprint 3

| Campo | Valor |
|-------|-------|
| Fechas | 06/05/2026 - 12/05/2026 |
| Objetivo | Mejorar la calidad, confianza y lectura analítica de los datos. |

### Historias incluidas

1. HU-06: Clasificar incidente por tipo y nivel de riesgo.
2. HU-07: Moderar incidentes reportados.
3. HU-08: Ver resumen de incidentes por comuna y tipo.

### Justificación de prioridad

Una vez implementado el flujo principal, estas historias aumentan el valor de los datos. La clasificación permite interpretar mejor los reportes, la moderación mejora su confiabilidad y el resumen facilita la toma de decisiones.

## Roadmap completo

| Sprint | Historias | Resultado esperado |
|--------|-----------|--------------------|
| Sprint 1 | HU-03, HU-04 | Flujo base de reporte y mapa. |
| Sprint 2 | HU-01, HU-02, HU-05 | Autenticación y consulta filtrada. |
| Sprint 3 | HU-06, HU-07, HU-08 | Datos más confiables y análisis básico. |
