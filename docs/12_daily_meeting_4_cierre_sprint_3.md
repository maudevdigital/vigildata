# Daily Meeting 4 - Taiga, cierre de Sprint 3 y preparacion del video Hito 2

Fecha de actualizacion: 19/05/2026  
Medio: Discord / Taiga  
Proyecto: VigilData - Ingenieria de Software 1  
Trabajo en Taiga: Ingenieria de software 1  
Product Owner: lucasmaulenr  
Tipo de registro: Daily Meeting en Taiga  

## Objetivo de la Daily Meeting

Revisar en Taiga el cierre de Sprint 3, confirmar el estado de las historias HU-06, HU-07 y HU-08, y dejar acordado el guion del video del Product Owner para la entrega del Hito 2.

El acuerdo para el video del Hito 2 mantiene las tres tecnicas de prueba ya usadas en el video anterior:

1. Pruebas de caja negra.
2. Pruebas de aceptacion.
3. Pruebas unitarias.

La ejecucion de las pruebas corresponde al Scrum Team, principalmente a los developers de frontend y backend. El Product Owner revisa la evidencia, valida los criterios de aceptacion y decide si una historia se puede aceptar.

## Estado de Taiga al 19/05/2026

Proyecto Taiga: Ingenieria de software 1  
Slug: `maudevdigital-ingenieria-de-software-1`  
ID de proyecto: `1786600`  
Fuente: consulta autenticada a la API de Taiga con el usuario `maudevdigital`.

| Sprint | Fechas planificadas | Estado en Taiga | Historias | Puntos cerrados |
|--------|---------------------|-----------------|-----------|-----------------|
| Sprint 1 | 20/04/2026 - 28/04/2026 | Cerrado | 2 | 100.0/100.0 |
| Sprint 2 | 29/04/2026 - 05/05/2026 | Cerrado | 3 | 150.0/150.0 |
| Sprint 3 | 06/05/2026 - 19/05/2026 | Cerrado | 3 | 100.0/100.0 |

Sprint 3 se extendio una semana respecto a la planificacion inicial (12/05) por dependencia de moderacion y resumen. Las tres historias HU-06, HU-07 y HU-08 figuran en estado Done. El total de tareas tecnicas asociadas al sprint es 15 y todas estan en estado Closed con commit asociado.

No hay issues registrados en Taiga al momento de la consulta directa.

## Historias cerradas en Sprint 3

| Ref. Taiga | Historia | Sprint | Estado | Asignado | Cerrada |
|------------|----------|--------|--------|----------|---------|
| #16 | HU-06: Clasificar incidente por tipo y nivel de riesgo | Sprint 3 | Done | Sebastian Lopez Cisternas | Si |
| #17 | HU-07: Moderar incidentes reportados | Sprint 3 | Done | Sebastian Lopez Cisternas | Si |
| #18 | HU-08: Ver resumen de incidentes por comuna y tipo | Sprint 3 | Done | benjaosan | Si |

## Evidencia de codigo por historia

| Historia | Commit principal | Archivos clave |
|----------|------------------|----------------|
| HU-06 | `8bdf725` | `vigildata-backend/app/models/incidente.py`, `app/schemas/incidente.py`, `vigildata-frontend/src/views/ReportarView.vue`, `views/MapaView.vue` |
| HU-07 | `8bdf725` | `app/routers/incidentes.py` (`PATCH /{id}/estado`), `views/AdminView.vue` |
| HU-08 | `102dd2f` (PR #7) | `app/routers/incidentes.py` (`GET /resumen`, helper `_aplicar_filtros`), `app/schemas/incidente.py` (`ConteoItem`, `IncidenteResumenResponse`), `src/components/IncidenteResumen.vue`, `views/MapaView.vue` |

Fix adicional aplicado durante la validacion de cierre (commit `5882711`): se especifico `foreign_keys` en la relacion `Usuario.incidentes` para resolver el error `AmbiguousForeignKeysError` introducido por la nueva FK `revisado_por_id` del modelo Incidente.

## Participacion del equipo

### lucasmaulenr - Product Owner

- Reviso el cierre de Sprint 3 en Taiga y valido que las tres historias quedaran en Done.
- Confirmo que cada tarea tecnica tuviera commit asociado como evidencia en el repositorio.
- Coordino el merge del PR #7 a main para integrar el resumen.
- Actualizo la wiki de Taiga con los documentos `sprint-3-cierre` y `hito-2-checklist`.
- Definio el guion del video del Hito 2 con la estructura sprint-por-sprint.

### benjaosan - Frontend

- Implemento el componente `IncidenteResumen.vue` con paneles por comuna y tipo (barras CSS).
- Integro el resumen al `MapaView.vue` para que se recargue junto con el listado al aplicar filtros.
- Valido el layout responsive del resumen (grid `grid-cols-1 md:grid-cols-2`).
- Ejecuta casos de caja negra del flujo de moderacion desde el `AdminView.vue`.

### Sebastian Lopez Cisternas - Back / ausente

- Figura en Taiga como responsable de HU-06 y HU-07 y de tareas backend asociadas.
- No se considera como expositor del video porque falto a la grabacion del Hito 1.
- Se menciona solo para mantener trazabilidad con el tablero de Taiga.

### Felipe Vergara R - Scrum Master / apoyo funcional

- Apoyo la revision funcional de la moderacion (estados pendiente/aprobado/rechazado).
- Reviso que los escenarios probados sean entendibles desde la mirada del usuario.
- Apoyo la preparacion de evidencia para el video del Hito 2.

## Tecnicas de prueba acordadas para Sprint 3

### 1. Pruebas de caja negra

Objetivo: evaluar el sistema desde fuera, sin revisar el codigo fuente, concentrandose en entradas, salidas, reglas de negocio y comportamiento esperado.

Responsable de ejecucion: Scrum Team / developers.  
Responsable de aceptacion del resultado: Product Owner.

| Historia | Caso de caja negra | Resultado esperado |
|----------|--------------------|-------------------|
| HU-06 | Reportar incidente con tipo y nivel de riesgo validos | Incidente creado con clasificacion |
| HU-06 | Reportar sin seleccionar nivel de riesgo | El sistema rechaza la entrada |
| HU-06 | Visualizar el mapa con incidentes de distintos niveles | Marcadores aparecen con color por nivel |
| HU-07 | Login con cuenta ANALISTA y aprobar un incidente pendiente | El incidente cambia a aprobado y aparece en el mapa publico |
| HU-07 | Login con cuenta CIUDADANO y cambiar estado de un incidente | Solicitud rechazada con HTTP 403 |
| HU-07 | Rechazar un incidente | El incidente desaparece del mapa publico |
| HU-08 | Consultar `/incidentes/resumen` sin filtros | Devuelve totales por comuna y por tipo |
| HU-08 | Consultar `/incidentes/resumen?comuna=Santiago` | Devuelve solo conteos de Santiago |
| HU-08 | Aplicar filtros en el mapa | El panel de resumen se actualiza junto con los marcadores |

Criterios derivados de caja negra:

- Particion de equivalencia: separar entradas validas e invalidas para tipo, nivel_riesgo y estado.
- Analisis de valores limite: probar bordes de rangos, por ejemplo el ultimo estado permitido en la transicion pendiente -> aprobado.

### 2. Pruebas de aceptacion

Objetivo: verificar que cada historia cumpla la necesidad del usuario y los criterios definidos por el Product Owner.

Responsable de ejecucion/demostracion: Scrum Team / developers.  
Responsable de aceptar o rechazar la historia: Product Owner.

| Historia | Escenario de aceptacion | Resultado esperado |
|----------|-------------------------|-------------------|
| HU-06 | Dado que soy un usuario autenticado, cuando reporto un incidente con tipo y nivel de riesgo, entonces el sistema lo guarda con esa clasificacion | Historia aceptable si los marcadores reflejan visualmente la clasificacion |
| HU-07 | Dado que soy un usuario con rol ANALISTA, cuando reviso un incidente pendiente, entonces puedo aprobarlo o rechazarlo y el cambio queda registrado con fecha y responsable | Historia aceptable si los incidentes rechazados no aparecen en el mapa publico |
| HU-08 | Dado que existen incidentes aprobados en distintas comunas y tipos, cuando consulto el resumen, entonces obtengo totales agrupados que respetan los filtros activos | Historia aceptable si los conteos coinciden con los marcadores visibles del mapa |

### 3. Pruebas unitarias

Objetivo: validar unidades pequenas del sistema, como funciones de backend, validaciones o logica de frontend, antes de integrarlas al flujo completo.

Responsable de ejecucion: developers del Scrum Team.  
Responsable de revisar evidencia funcional: Product Owner, cuando corresponda a criterios de aceptacion.

| Area | Unidad a probar | Resultado esperado |
|------|-----------------|-------------------|
| Backend | Validacion de nivel_riesgo en `IncidenteCreate` | Rechaza valores fuera del enum permitido |
| Backend | Endpoint `PATCH /incidentes/{id}/estado` con rol CIUDADANO | Devuelve HTTP 403 |
| Backend | Helper `_aplicar_filtros` con filtro por estado | Devuelve solo incidentes con estado coincidente |
| Backend | Endpoint `/incidentes/resumen` con incidentes aprobados | Conteos por comuna y por tipo correctos |
| Frontend | Click en mapa abre modal de reporte | Modal se monta con coordenadas del click |
| Frontend | `IncidenteResumen.vue` con datos vacios | Renderiza mensaje "No hay incidentes" sin romperse |

La cobertura actual del backend es 78.75%, por encima del minimo 60% exigido por el taller de testing unitario.

## Validacion end-to-end ejecutada el 19/05/2026

Se ejecuto una prueba completa con backend en SQLite local y frontend Vite dev. Resultados:

- Registro y login de ciudadano OK con rol CIUDADANO.
- Login del admin seed `admin@vigildata.cl` / `admin123` OK con rol ANALISTA.
- Creacion de 4 incidentes en 3 comunas con 3 niveles diferentes: OK.
- Moderacion: 3 aprobados y 1 rechazado: OK.
- `GET /incidentes/` esconde rechazados por defecto: OK.
- `GET /incidentes/resumen` devuelve totales correctos: OK.
- `GET /incidentes/resumen?comuna=Santiago` aplica filtro: OK.
- `GET /incidentes/resumen?estado=todos` incluye rechazados: OK.
- Click en mapa abre modal y crea incidente sin ir a /reportar: OK.
- Tras crear, el mapa centra en el nuevo punto: OK.

## Acuerdos de la Daily Meeting 4

- Sprint 3 se presenta como cerrado en Taiga con las tres historias en Done.
- El video del Hito 2 mostrara los tres sprints en orden, con foco en Sprint 3 al final.
- Las tecnicas de prueba del video seguiran siendo caja negra, aceptacion y unitarias.
- Los developers/Scrum Team ejecutan o demuestran las pruebas; el Product Owner valida los criterios.
- Para la demo se usara la base SQLite local (`vigildata-backend/local-demo.db`) porque el proyecto Supabase original fue eliminado. Esta decision quedo documentada en README.md y en `.env.example`.
- Sebastian Lopez Cisternas se menciona solo por trazabilidad, pero no se considera como expositor porque falto a la grabacion del Hito 1.
- No hay issues formales registrados en Taiga.

## Cierre de la Daily Meeting

Como Product Owner, el cierre del Sprint 3 muestra que el producto ya permite:

1. Reportar incidentes con clasificacion por tipo y nivel de riesgo.
2. Visualizar incidentes con colores diferenciados por nivel.
3. Moderar incidentes pendientes desde el panel de administracion.
4. Ocultar incidentes rechazados del mapa publico.
5. Consultar resumenes agrupados por comuna y por tipo, respetando los filtros activos del mapa.
6. Crear un reporte con un solo click sobre el mapa (mejora UX agregada durante el Sprint 3).

Para el video del Hito 2, la explicacion debe conectar historias, criterios de aceptacion y pruebas en los tres sprints. Caja negra valida comportamiento observable; aceptacion confirma valor para el usuario; unitarias garantizan que las unidades del backend (filtros, agregaciones, control de roles) y del frontend (formulario de reporte, panel de resumen) se comportan correctamente antes de integrarse al flujo completo.
