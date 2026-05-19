# Guion completo de video - Equipo - Sprint 1 y Sprint 2

Proyecto: VigilData  
Trabajo en Taiga: Ingenieria de software 1  
Fecha de referencia: 03/05/2026  
Estado base: Sprint 1 cerrado, Sprint 2 cerrado, Sprint 3 abierto  

> Nota: este guion considera como expositores a Lucas, Felipe y benjaosan. Sebastian Lopez Cisternas figura en Taiga como Back y tiene tareas asociadas, pero no se considera como expositor porque falto a la grabacion. Se menciona solo brevemente por trazabilidad del tablero.

## 1. Distribucion del video

| Integrante | Rol para el video | Que presenta |
|------------|-------------------|--------------|
| Lucas Maulen | Product Owner | Proyecto, equipo, vision, backlog, priorizacion, valor de Sprint 1 y Sprint 2, cierre |
| Felipe Vergara R | Scrum Master | Uso de Taiga, estado de sprints, Daily Meeting, coordinacion y pruebas acordadas |
| benjaosan | Frontend / Developer | Flujo visible del producto: registro, login, reporte, mapa y filtros |
| Sebastian Lopez Cisternas | Back / ausente | No expone; se menciona solo porque aparece en Taiga con tareas backend |

## 2. Apertura - Lucas, Product Owner

Hola, soy Lucas Maulen y en el proyecto VigilData cumplo el rol de Product Owner.

En este video vamos a presentar el avance del proyecto hasta Sprint 2, usando la informacion registrada en Taiga en el proyecto `Ingenieria de software 1`.

Primero presento al equipo. Yo participo como Product Owner, encargado de priorizar el backlog, cuidar el valor del producto y validar criterios de aceptacion. Felipe Vergara cumple el rol de Scrum Master, apoyando la coordinacion del equipo, el seguimiento en Taiga y la organizacion de las reuniones. benjaosan participa como developer frontend, trabajando en la interfaz y en la experiencia visible para el usuario.

Sebastian Lopez Cisternas aparece en Taiga como integrante backend y tiene tareas asociadas al desarrollo, pero para este video no lo consideraremos como expositor porque falto a la grabacion. Lo mencionamos solo para mantener la trazabilidad con el tablero.

VigilData es una aplicacion web orientada a seguridad ciudadana. Su objetivo es que los vecinos puedan reportar incidentes con ubicacion geografica y que otros usuarios puedan visualizarlos en un mapa interactivo. La idea principal es transformar informacion dispersa del barrio en datos utiles para consultar zonas de riesgo y tomar mejores decisiones.

## 3. Vision del producto - Lucas

La vision de VigilData es construir un mapa colaborativo de seguridad ciudadana.

Para esta etapa definimos un MVP, es decir, una primera version funcional que resolviera el flujo central del producto. Ese flujo consiste en que un usuario pueda registrarse, iniciar sesion, reportar un incidente con ubicacion GPS, guardar informacion relevante del incidente y visualizar esos reportes en un mapa.

Desde el rol de Product Owner, esta definicion fue importante porque nos permitio separar lo esencial de lo secundario. Para los primeros sprints no era necesario incluir analitica avanzada, moderacion o resumen estadistico. Primero necesitabamos validar que el producto cumpliera su objetivo principal: reportar y visualizar incidentes.

## 4. Product Backlog y priorizacion - Lucas

El Product Backlog se organizo en ocho historias de usuario.

Para el Sprint 1 se priorizaron dos historias:

- HU-03: Reportar incidente con GPS.
- HU-04: Ver mapa con incidentes.

Estas historias quedaron primero porque representan el nucleo del producto. Si VigilData no permite reportar incidentes y visualizarlos en un mapa, entonces no cumple su proposito.

Para el Sprint 2 se priorizaron tres historias:

- HU-01: Registro de usuario con email.
- HU-02: Inicio de sesion con JWT.
- HU-05: Filtrar incidentes por comuna y fecha.

Estas historias fortalecen el uso real del sistema. El registro y login permiten identificar al usuario y proteger acciones sensibles. Los filtros permiten que el mapa sea una herramienta de consulta mas util, porque el usuario puede buscar informacion por comuna y por rango de fechas.

Mi criterio de priorizacion fue avanzar desde el valor minimo visible hacia mayor confianza y utilidad: primero reporte y mapa; despues autenticacion y filtros.

## 5. Estado de Taiga y Daily Meeting - Felipe, Scrum Master

Desde el rol de Scrum Master, revise el estado del proyecto en Taiga para mantener alineado al equipo.

El proyecto en Taiga se llama `Ingenieria de software 1`, con slug `maudevdigital-ingenieria-de-software-1`.

Al revisar el tablero, el estado es el siguiente:

| Sprint | Fechas | Estado en Taiga | Historias |
|--------|--------|-----------------|-----------|
| Sprint 1 | 20/04/2026 - 28/04/2026 | Cerrado | HU-03, HU-04 |
| Sprint 2 | 29/04/2026 - 05/05/2026 | Cerrado | HU-01, HU-02, HU-05 |
| Sprint 3 | 06/05/2026 - 12/05/2026 | Abierto | HU-06, HU-07, HU-08 |

En la Daily Meeting 3 se reviso que Sprint 1 y Sprint 2 quedaran cerrados, que las historias hasta HU-05 estuvieran en estado Done y que no existieran issues formales registrados.

Tambien se acordo que el video debe enfocarse en el avance real hasta Sprint 2. Sprint 3 se puede mencionar como trabajo futuro, pero no como funcionalidad terminada.

## 6. Sprint 1 - Lucas

El Sprint 1 se desarrollo entre el 20/04/2026 y el 28/04/2026. Su objetivo fue implementar el flujo principal de reporte y visualizacion de incidentes.

Las historias incluidas fueron:

- HU-03: Como usuario autenticado, quiero reportar un incidente usando mi ubicacion GPS para alertar a otros ciudadanos sobre situaciones de riesgo en mi zona.
- HU-04: Como ciudadano, quiero ver un mapa interactivo con los incidentes reportados para conocer las zonas de riesgo cercanas a mi ubicacion.

Para HU-03, los criterios de aceptacion principales fueron capturar tipo, descripcion, latitud, longitud y comuna; obtener ubicacion con Geolocation API; exigir token valido para crear reportes; y guardar fecha y hora del servidor.

Para HU-04, los criterios fueron cargar el mapa con Leaflet, mostrar incidentes como marcadores, desplegar informacion en un popup y mantener una vista responsive.

El valor entregado por Sprint 1 fue dejar funcionando la base del producto: crear un reporte de incidente y verlo reflejado en un mapa.

## 7. Demostracion funcional de Sprint 1 - benjaosan

Desde la parte frontend, en Sprint 1 el foco estuvo en que el usuario pudiera interactuar con el producto de forma clara.

Primero, se preparo el flujo de reporte de incidente, donde el usuario ingresa los datos necesarios y permite obtener su ubicacion GPS. Luego, esos datos se relacionan con el mapa, para que el incidente pueda aparecer como un punto georreferenciado.

En la demostracion del video se puede mostrar el mapa con marcadores y explicar que cada marcador representa un incidente reportado. Al abrir un marcador, el usuario deberia ver informacion util, como tipo de incidente, descripcion, fecha y comuna.

Esta parte es importante porque hace visible el valor principal de VigilData: transformar un reporte ciudadano en informacion ubicable dentro del mapa.

## 8. Sprint 2 - Lucas

El Sprint 2 fue planificado entre el 29/04/2026 y el 05/05/2026. En Taiga aparece cerrado, con HU-01, HU-02 y HU-05 en estado Done.

El objetivo del Sprint 2 fue incorporar autenticacion y filtros para mejorar el uso real de los reportes.

Las historias incluidas fueron:

- HU-01: Registro de usuario con email.
- HU-02: Inicio de sesion con JWT.
- HU-05: Filtrar incidentes por comuna y fecha.

El valor de este sprint fue pasar de un prototipo funcional a un sistema mas confiable. Con registro e inicio de sesion, los reportes pueden asociarse a usuarios. Con filtros por comuna y fecha, el mapa deja de ser solo una visualizacion general y se convierte en una herramienta de consulta.

Como Product Owner, mi responsabilidad fue validar que estas historias respondieran a criterios de aceptacion concretos: crear cuenta, iniciar sesion, recibir token, proteger acciones sensibles y filtrar resultados correctamente.

## 9. Demostracion funcional de Sprint 2 - benjaosan

En Sprint 2, desde la experiencia del usuario, el flujo se completa con tres elementos principales.

Primero, el registro de usuario. El sistema debe permitir ingresar email y contrasena, validar datos y evitar registros duplicados.

Segundo, el inicio de sesion. El usuario debe ingresar credenciales validas y recibir acceso mediante un token JWT. Esto permite proteger acciones como reportar incidentes.

Tercero, los filtros. El usuario debe poder filtrar incidentes por comuna, por rango de fechas o combinando ambos criterios. Esto mejora la utilidad del mapa, porque permite consultar informacion segun el contexto del ciudadano.

En el video, esta parte puede mostrarse como una navegacion breve: registro o login, acceso al mapa, visualizacion de incidentes y uso de filtros.

## 10. Pruebas acordadas - Felipe, Scrum Master

Para las pruebas del proyecto se acordaron tres tecnicas: pruebas de caja negra, pruebas de aceptacion y pruebas unitarias.

La ejecucion o demostracion de las pruebas corresponde al Scrum Team, principalmente a los developers. El Product Owner valida la evidencia contra los criterios de aceptacion.

Las pruebas de caja negra permiten evaluar el sistema desde fuera, sin revisar el codigo interno. Se prueban entradas, salidas y comportamiento esperado.

Ejemplos aplicados a VigilData:

| Historia | Caso de caja negra | Resultado esperado |
|----------|--------------------|-------------------|
| HU-01 | Registrar email valido y contrasena valida | Cuenta creada correctamente |
| HU-01 | Registrar email duplicado | Error controlado |
| HU-02 | Login con credenciales validas | Se entrega token JWT |
| HU-02 | Login con contrasena incorrecta | Acceso rechazado |
| HU-03 | Reportar incidente con campos completos y GPS permitido | Incidente creado |
| HU-03 | Reportar incidente sin token valido | Solicitud rechazada |
| HU-04 | Abrir mapa con incidentes existentes | Marcadores visibles |
| HU-05 | Filtrar por comuna y rango de fechas | Resultados filtrados correctamente |

Estas pruebas ayudan al equipo a comprobar el comportamiento visible del producto.

Las pruebas unitarias quedan a cargo de los developers. Sirven para validar piezas pequenas del sistema antes de integrarlas al flujo completo.

Ejemplos aplicados a VigilData:

| Area | Unidad a probar | Resultado esperado |
|------|-----------------|-------------------|
| Backend | Funcion que genera token JWT | Devuelve un token valido para credenciales correctas |
| Backend | Validacion de credenciales | Rechaza password incorrecta o usuario inexistente |
| Backend | Funcion de filtros | Devuelve incidentes segun comuna y rango de fechas |
| Frontend | Validacion de formulario de registro | Detecta email invalido o campos obligatorios vacios |
| Frontend | Logica de filtros del mapa | Construye correctamente los parametros de busqueda |

Estas pruebas no reemplazan la aceptacion del Product Owner, pero entregan evidencia tecnica de que las partes internas principales funcionan antes de la demostracion.

## 11. Pruebas de aceptacion - Lucas

Las pruebas de aceptacion son las mas cercanas a mi rol como Product Owner, porque permiten decidir si una historia cumple la necesidad del usuario y puede darse por terminada.

Para VigilData, las pruebas de aceptacion se pueden expresar asi:

| Historia | Escenario de aceptacion | Resultado esperado |
|----------|-------------------------|-------------------|
| HU-01 | Dado que soy un ciudadano sin cuenta, cuando registro email y contrasena validos, entonces el sistema crea mi cuenta | La historia se acepta si el registro funciona y evita duplicados |
| HU-02 | Dado que soy un usuario registrado, cuando inicio sesion con credenciales validas, entonces recibo un token JWT | La historia se acepta si el login permite acceder a funciones protegidas |
| HU-03 | Dado que soy un usuario autenticado, cuando reporto un incidente con GPS, entonces el sistema guarda el incidente | La historia se acepta si el reporte queda registrado correctamente |
| HU-04 | Dado que existen incidentes registrados, cuando abro el mapa, entonces veo marcadores con informacion util | La historia se acepta si los reportes se visualizan en el mapa |
| HU-05 | Dado que existen incidentes en distintas comunas y fechas, cuando aplico filtros, entonces solo veo los incidentes correspondientes | La historia se acepta si los filtros devuelven resultados coherentes |

Con estas pruebas, el equipo no valida solo que haya codigo, sino que cada historia entregue valor real al usuario.

## 12. Cierre del equipo - Lucas

Para cerrar, el avance hasta Sprint 2 muestra que VigilData ya cumple su flujo principal.

Primero, Sprint 1 permitio reportar incidentes y visualizarlos en un mapa. Segundo, Sprint 2 incorporo registro, inicio de sesion y filtros, fortaleciendo la confianza y utilidad del producto. Tercero, las pruebas acordadas, caja negra, aceptacion y unitarias, permiten validar el comportamiento visible, aceptar historias contra criterios y comprobar unidades tecnicas del sistema.

Como Product Owner, mi foco fue asegurar que el equipo trabajara sobre valor, alcance claro y criterios de aceptacion verificables. Como Scrum Master, Felipe apoyo la organizacion, seguimiento y acuerdos del equipo. Desde frontend, benjaosan trabajo el flujo visible que permite al usuario interactuar con el producto.

Con esto, VigilData avanza como un MVP coherente: permite registrar usuarios, iniciar sesion, reportar incidentes, verlos en el mapa y filtrarlos por comuna y fecha.

## 13. Checklist para grabar

- Lucas abre el video, presenta el proyecto y al equipo.
- Lucas menciona brevemente que Sebastian figura en Taiga como backend, pero no expone porque falto a la grabacion.
- Lucas explica vision, backlog, priorizacion y valor del producto.
- Felipe explica Taiga, Daily Meeting, estado de sprints y acuerdos de pruebas.
- benjaosan explica el flujo visible del producto: registro, login, reporte, mapa y filtros.
- Lucas explica pruebas de aceptacion y cierre como Product Owner.
- Usar tres tecnicas de prueba: caja negra, aceptacion y unitarias.
- No presentar Sprint 3 como terminado; mencionarlo solo como trabajo futuro.
