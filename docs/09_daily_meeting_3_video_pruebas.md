# Daily Meeting 3 - Taiga, cierre de Sprint 2 y pruebas

Fecha de actualizacion: 03/05/2026  
Medio: Discord / Taiga  
Proyecto: VigilData - Ingenieria de Software 1  
Trabajo en Taiga: Ingenieria de software 1  
Product Owner: lucasmaulenr  
Tipo de registro: Daily Meeting en Taiga  

## Objetivo de la Daily Meeting

Revisar en Taiga el cierre de Sprint 1 y Sprint 2, confirmar el estado de las historias comprometidas y dejar acordado que tecnicas de prueba se explicaran en el video del Product Owner.

El acuerdo para el video es usar tres tecnicas de prueba:

1. Pruebas de caja negra.
2. Pruebas de aceptacion.
3. Pruebas unitarias.

La ejecucion de las pruebas corresponde al Scrum Team, principalmente a los developers de frontend y backend. El Product Owner revisa la evidencia, valida los criterios de aceptacion y decide si una historia se puede aceptar.

## Estado de Taiga al 03/05/2026

Proyecto Taiga: Ingenieria de software 1  
Slug: `maudevdigital-ingenieria-de-software-1`  
ID de proyecto: `1786600`  
Fuente: consulta autenticada a la API de Taiga con el usuario `maudevdigital`.

| Sprint | Fechas planificadas | Estado en Taiga | Historias | Puntos cerrados |
|--------|---------------------|-----------------|-----------|-----------------|
| Sprint 1 | 20/04/2026 - 28/04/2026 | Cerrado | 2 | 100.0/100.0 |
| Sprint 2 | 29/04/2026 - 05/05/2026 | Cerrado | 3 | 150.0/150.0 |
| Sprint 3 | 06/05/2026 - 12/05/2026 | Abierto | 3 | Sin puntos cerrados |

Sprint 1 aparece cerrado en Taiga. Las historias HU-03 y HU-04 figuran en estado Done y cerradas.

Sprint 2 tambien aparece cerrado en Taiga. Las historias HU-01, HU-02 y HU-05 figuran en estado Done y cerradas, con cierre registrado el 01/05/2026.

Sprint 3 aparece abierto. Las historias HU-06, HU-07 y HU-08 siguen en estado New, por lo que no se deben presentar como funcionalidades terminadas en el video.

No hay issues registrados en Taiga al momento de la consulta directa.

## Historias cerradas hasta Sprint 2

| Ref. Taiga | Historia | Sprint | Estado | Asignado | Cerrada |
|------------|----------|--------|--------|----------|---------|
| #1 | HU-01: Registro de usuario con email | Sprint 2 | Done | benjaosan | Si |
| #2 | HU-02: Inicio de sesion con JWT | Sprint 2 | Done | Sebastian Lopez Cisternas | Si |
| #3 | HU-03: Reportar incidente con GPS | Sprint 1 | Done | Sebastian Lopez Cisternas | Si |
| #4 | HU-04: Ver mapa con incidentes | Sprint 1 | Done | benjaosan | Si |
| #5 | HU-05: Filtrar incidentes por comuna y fecha | Sprint 2 | Done | Sebastian Lopez Cisternas | Si |

## Historias futuras no cerradas

| Ref. Taiga | Historia | Sprint | Estado | Asignado | Cerrada |
|------------|----------|--------|--------|----------|---------|
| #16 | HU-06: Clasificar incidente por tipo y nivel de riesgo | Sprint 3 | New | Sebastian Lopez Cisternas | No |
| #17 | HU-07: Moderar incidentes reportados | Sprint 3 | New | Sebastian Lopez Cisternas | No |
| #18 | HU-08: Ver resumen de incidentes por comuna y tipo | Sprint 3 | New | benjaosan | No |

## Participacion del equipo

### lucasmaulenr - Product Owner

- Priorizo el Product Backlog segun valor de producto.
- Confirmo el estado de Sprint 1 y Sprint 2 en Taiga.
- Reviso que las historias cerradas correspondan al alcance del MVP hasta Sprint 2.
- Define criterios de aceptacion y valida si las historias pueden aceptarse.
- Presenta en el video la relacion entre backlog, sprints, criterios de aceptacion y pruebas.

### benjaosan - Frontend

- Implementa y prueba funcionalidades visibles para el usuario.
- Valida pantallas de registro, inicio de sesion, mapa y filtros desde la interfaz.
- Ejecuta casos de caja negra asociados a comportamiento observable del frontend.

### Sebastian Lopez Cisternas - Back / ausente

- Figura en Taiga como integrante backend y tiene tareas asociadas.
- No se considera como expositor del video porque falto a la grabacion.
- Se menciona solo para mantener trazabilidad con el tablero de Taiga.

### Felipe Vergara R - Scrum Master / apoyo funcional

- Apoya la revision funcional del flujo.
- Revisa que los escenarios probados sean entendibles desde la mirada del usuario.
- Apoya la preparacion de evidencia para el video.

## Tecnicas de prueba acordadas

### 1. Pruebas de caja negra

Objetivo: evaluar el sistema desde fuera, sin revisar el codigo fuente, concentrandose en entradas, salidas, reglas de negocio y comportamiento esperado.

Responsable de ejecucion: Scrum Team / developers.  
Responsable de aceptacion del resultado: Product Owner.

| Historia | Caso de caja negra | Resultado esperado |
|----------|--------------------|-------------------|
| HU-01 | Registrar email valido y contrasena valida | Cuenta creada correctamente |
| HU-01 | Registrar email duplicado | Error controlado |
| HU-01 | Registrar email con formato invalido | El sistema rechaza la entrada |
| HU-02 | Login con credenciales validas | Se entrega token JWT |
| HU-02 | Login con contrasena incorrecta | Acceso rechazado con error controlado |
| HU-03 | Reportar incidente con campos completos y GPS permitido | Incidente creado |
| HU-03 | Reportar incidente sin token valido | Solicitud rechazada |
| HU-04 | Abrir mapa con incidentes existentes | Marcadores visibles |
| HU-04 | Abrir popup de marcador | Informacion del incidente visible |
| HU-05 | Filtrar por comuna existente | Se muestran incidentes de esa comuna |
| HU-05 | Filtrar por comuna sin datos | Lista o mapa sin resultados |
| HU-05 | Filtrar por comuna y rango de fechas | Se muestran solo incidentes que cumplen ambos filtros |

Criterios derivados de caja negra:

- Particion de equivalencia: separar datos validos e invalidos, por ejemplo emails validos e invalidos.
- Analisis de valores limite: probar bordes de rangos, por ejemplo fechas exactas de inicio y termino.

### 2. Pruebas de aceptacion

Objetivo: verificar que cada historia cumpla la necesidad del usuario y los criterios definidos por el Product Owner.

Responsable de ejecucion/demostracion: Scrum Team / developers.  
Responsable de aceptar o rechazar la historia: Product Owner.

| Historia | Escenario de aceptacion | Resultado esperado |
|----------|-------------------------|-------------------|
| HU-01 | Dado que soy un ciudadano sin cuenta, cuando registro email y contrasena validos, entonces el sistema crea mi cuenta | Historia aceptable si el registro funciona y evita duplicados |
| HU-02 | Dado que soy un usuario registrado, cuando inicio sesion con credenciales validas, entonces recibo un token JWT | Historia aceptable si el login permite acceder a funciones protegidas |
| HU-03 | Dado que soy un usuario autenticado, cuando reporto un incidente con GPS, entonces el sistema guarda el incidente | Historia aceptable si el reporte queda registrado correctamente |
| HU-04 | Dado que existen incidentes registrados, cuando abro el mapa, entonces veo marcadores con informacion util | Historia aceptable si los reportes se visualizan en el mapa |
| HU-05 | Dado que existen incidentes en distintas comunas y fechas, cuando aplico filtros, entonces solo veo los incidentes correspondientes | Historia aceptable si los filtros devuelven resultados coherentes |

### 3. Pruebas unitarias

Objetivo: validar unidades pequenas del sistema, como funciones de backend, validaciones o logica de frontend, antes de integrarlas al flujo completo.

Responsable de ejecucion: developers del Scrum Team.  
Responsable de revisar evidencia funcional: Product Owner, cuando corresponda a criterios de aceptacion.

| Area | Unidad a probar | Resultado esperado |
|------|-----------------|-------------------|
| Backend | Generacion de token JWT | Devuelve token valido con credenciales correctas |
| Backend | Validacion de credenciales | Rechaza password incorrecta o usuario inexistente |
| Backend | Filtros de incidentes | Devuelve datos segun comuna y rango de fechas |
| Frontend | Validacion de formulario de registro | Detecta email invalido y campos obligatorios vacios |
| Frontend | Logica de filtros del mapa | Envia correctamente comuna, fecha_inicio y fecha_fin |

## Acuerdos de la Daily Meeting 3

- Sprint 1 y Sprint 2 se presentaran como cerrados en Taiga.
- Sprint 3 se mencionara solo como trabajo futuro o no cerrado.
- Las tecnicas de prueba del video seran caja negra, aceptacion y unitarias.
- Los developers/Scrum Team ejecutan o demuestran las pruebas.
- El Product Owner valida los criterios de aceptacion y decide si las historias se aceptan.
- Sebastian Lopez Cisternas se menciona solo por trazabilidad, pero no se considera como expositor porque falto a la grabacion.
- No hay issues formales registrados en Taiga.

## Cierre de la Daily Meeting

Como Product Owner, el cierre hasta Sprint 2 consiste en mostrar que el producto ya permite:

1. Registrar usuarios.
2. Iniciar sesion con JWT.
3. Reportar incidentes protegidos por autenticacion.
4. Visualizar incidentes en mapa.
5. Filtrar incidentes por comuna y fecha.

Para el video, la explicacion debe conectar historias, criterios de aceptacion y pruebas. Caja negra valida el comportamiento observable del sistema; aceptacion confirma si ese comportamiento cumple el valor esperado por el usuario.
