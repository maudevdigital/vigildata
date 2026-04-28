# Product Backlog - VigilData

## Backlog priorizado

| Ref. Taiga | Historia de usuario | Prioridad | Sprint |
|------------|---------------------|-----------|--------|
| HU-03 | Reportar incidente con GPS | Alta | Sprint 1 |
| HU-04 | Ver mapa con incidentes | Alta | Sprint 1 |
| HU-01 | Registro de usuario con email | Alta | Sprint 2 |
| HU-02 | Inicio de sesión con JWT | Alta | Sprint 2 |
| HU-05 | Filtrar incidentes por comuna y fecha | Media alta | Sprint 2 |
| HU-06 | Clasificar incidente por tipo y nivel de riesgo | Media alta | Sprint 3 |
| HU-07 | Moderar incidentes reportados | Media | Sprint 3 |
| HU-08 | Ver resumen de incidentes por comuna y tipo | Media | Sprint 3 |

## HU-01: Registro de usuario con email

Como ciudadano, quiero registrarme con mi email para poder acceder a funcionalidades que requieren identificación.

### Criterios de aceptación

- El sistema permite registrar nombre, email y contraseña.
- El email debe ser único.
- La contraseña se almacena de forma segura.
- El usuario registrado puede iniciar sesión posteriormente.

## HU-02: Inicio de sesión con JWT

Como usuario registrado, quiero iniciar sesión y recibir un token JWT para acceder a funcionalidades protegidas.

### Criterios de aceptación

- El usuario puede iniciar sesión con email y contraseña.
- El sistema entrega un token JWT válido.
- El token permite acceder a endpoints protegidos.
- Las credenciales incorrectas retornan un error controlado.

## HU-03: Reportar incidente con GPS

Como usuario autenticado, quiero reportar un incidente usando mi ubicación GPS para alertar a otros ciudadanos sobre situaciones de riesgo en mi zona.

### Criterios de aceptación

- El formulario captura tipo, descripción, latitud, longitud y comuna.
- La ubicación puede obtenerse automáticamente mediante Geolocation API.
- Solo usuarios con token válido pueden crear reportes.
- El incidente queda almacenado con fecha y hora del servidor.

## HU-04: Ver mapa con incidentes

Como ciudadano, quiero ver un mapa interactivo con los incidentes reportados para conocer las zonas de riesgo cercanas a mi ubicación.

### Criterios de aceptación

- El mapa carga con Leaflet centrado en Chile.
- Los incidentes se muestran como marcadores con popup informativo.
- Los marcadores muestran tipo, descripción, fecha y comuna.
- El mapa es responsive y usable en móvil.

## HU-05: Filtrar incidentes por comuna y fecha

Como ciudadano, quiero filtrar incidentes por comuna y fecha para consultar información relevante a mi contexto.

### Criterios de aceptación

- El usuario puede filtrar por comuna.
- El usuario puede filtrar por rango de fechas.
- Los filtros actualizan los incidentes visibles en el mapa.
- Los filtros pueden combinarse.

## HU-06: Clasificar incidente por tipo y nivel de riesgo

Como usuario autenticado, quiero clasificar el incidente por tipo y nivel de riesgo para que otros ciudadanos puedan interpretar mejor la gravedad de la situación reportada.

### Criterios de aceptación

- El reporte permite seleccionar un tipo de incidente.
- El reporte permite seleccionar un nivel de riesgo: bajo, medio o alto.
- El tipo y el nivel de riesgo quedan almacenados junto al incidente.
- El mapa puede usar esta información para diferenciar visualmente los reportes.

## HU-07: Moderar incidentes reportados

Como administrador o moderador, quiero revisar incidentes reportados antes de destacarlos en el mapa para reducir información falsa, duplicada o irrelevante.

### Criterios de aceptación

- Cada incidente tiene un estado: pendiente, aprobado o rechazado.
- Un usuario con rol autorizado puede cambiar el estado del incidente.
- Los incidentes rechazados no se muestran como reportes activos en el mapa.
- El cambio de estado queda registrado con fecha y usuario responsable.

## HU-08: Ver resumen de incidentes por comuna y tipo

Como ciudadano, quiero ver un resumen de incidentes agrupados por comuna y tipo para comprender rápidamente qué zonas y situaciones presentan mayor riesgo.

### Criterios de aceptación

- El sistema muestra totales de incidentes por comuna.
- El sistema muestra totales por tipo de incidente.
- El resumen respeta los filtros de comuna y fecha cuando estén activos.
- La visualización es clara y usable en escritorio y móvil.
