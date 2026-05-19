# Requisitos y criterios de aceptación

## Requisitos funcionales

| ID | Requisito | Historias relacionadas |
|----|-----------|------------------------|
| RF-01 | El sistema debe permitir registrar usuarios. | HU-01 |
| RF-02 | El sistema debe permitir iniciar sesión con JWT. | HU-02 |
| RF-03 | El sistema debe permitir reportar incidentes con ubicación GPS. | HU-03 |
| RF-04 | El sistema debe visualizar incidentes en un mapa. | HU-04 |
| RF-05 | El sistema debe permitir filtrar incidentes por comuna y fecha. | HU-05 |
| RF-06 | El sistema debe clasificar incidentes por tipo y nivel de riesgo. | HU-06 |
| RF-07 | El sistema debe permitir moderar incidentes reportados. | HU-07 |
| RF-08 | El sistema debe mostrar resúmenes por comuna y tipo de incidente. | HU-08 |

## Requisitos no funcionales

| ID | Requisito |
|----|-----------|
| RNF-01 | La interfaz debe ser responsive y usable en dispositivos móviles. |
| RNF-02 | Los endpoints protegidos deben validar token JWT. |
| RNF-03 | La fecha y hora de incidentes deben registrarse desde el servidor. |
| RNF-04 | El mapa debe cargar de forma clara y legible usando Leaflet. |
| RNF-05 | Los datos sensibles de usuario no deben exponerse en respuestas públicas. |

## Criterios generales de aceptación

- Las funcionalidades implementadas deben corresponder a las historias priorizadas por sprint.
- Cada historia debe tener criterios de aceptación verificables.
- El tablero de Taiga debe reflejar el estado real del avance.
- El flujo mínimo de producto debe permitir registrar, reportar, visualizar y filtrar incidentes.

## Tecnicas de prueba acordadas

Para validar las historias de Sprint 1 y Sprint 2 se consideran tres tecnicas:

1. Pruebas de caja negra: validan entradas, salidas y comportamiento visible del sistema.
2. Pruebas de aceptacion: verifican si cada historia cumple los criterios definidos por el Product Owner.
3. Pruebas unitarias: validan unidades pequenas del backend o frontend, como generacion de JWT, validaciones de formularios y logica de filtros.

La ejecucion de las pruebas corresponde al Scrum Team/developers. El Product Owner revisa evidencia funcional y acepta las historias contra criterios de aceptacion.

## Trazabilidad por sprint

| Sprint | Historias | Requisitos principales |
|--------|-----------|------------------------|
| Sprint 1 | HU-03, HU-04 | RF-03, RF-04, RNF-01, RNF-04 |
| Sprint 2 | HU-01, HU-02, HU-05 | RF-01, RF-02, RF-05, RNF-02 |
| Sprint 3 | HU-06, HU-07, HU-08 | RF-06, RF-07, RF-08, RNF-05 |
