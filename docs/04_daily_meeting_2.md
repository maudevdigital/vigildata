# Daily Meeting 2

Fecha: 27/04/2026  
Hora: 18:00 horas  
Medio: Discord  
Proyecto: VigilData - Ingeniería de Software 1  
Sprint: Sprint 1  
Cierre del sprint: 28/04/2026  

## Objetivo de la reunión

Revisar el avance del Scrum Team sobre las historias comprometidas para el Sprint 1 y definir las tareas necesarias para llegar al cierre del sprint el 28/04/2026.

## Historias del Sprint 1

### HU-03: Reportar incidente con GPS

Como usuario autenticado, quiero reportar un incidente usando mi ubicación GPS para alertar a otros ciudadanos sobre situaciones de riesgo en mi zona.

### HU-04: Ver mapa con incidentes

Como ciudadano, quiero ver un mapa interactivo con los incidentes reportados para conocer las zonas de riesgo cercanas a mi ubicación.

## Estado actual

- El Sprint 1 se encuentra activo.
- Las historias HU-03 y HU-04 están dentro del sprint.
- Ambas historias figuran en estado New en Taiga.
- No hay issues registrados.
- No hay bloqueos formales registrados.
- Ya se crearon tareas técnicas asociadas a las historias del sprint.

## Participación del Scrum Team

### benjaosan - Frontend

Ayer:

- Revisó el alcance visual de HU-03 y HU-04.
- Identificó que el flujo principal debe permitir reportar incidentes y visualizarlos en mapa.

Hoy:

- Crear el formulario para reportar incidentes.
- Integrar Geolocation API para obtener latitud y longitud.
- Crear la vista de mapa usando Leaflet.
- Mostrar incidentes como marcadores.
- Agregar popup informativo con tipo, descripción, fecha y comuna.
- Validar que la interfaz sea responsive y usable en móvil.

Bloqueos:

- Depende del formato de datos entregado por backend para listar incidentes en el mapa.

### Sebastián López Cisternas - Backend

Ayer:

- Revisó los datos necesarios para soportar HU-03.
- Identificó los campos mínimos del incidente: tipo, descripción, latitud, longitud, comuna, fecha/hora y usuario.

Hoy:

- Definir el modelo de datos para incidentes.
- Crear endpoint para registrar un incidente.
- Validar token de usuario antes de permitir el reporte.
- Guardar fecha y hora desde el servidor.
- Crear endpoint para listar incidentes disponibles para el mapa.
- Definir junto a frontend el formato JSON de respuesta.

Bloqueos:

- Requiere coordinación con frontend para acordar estructura de datos y campos obligatorios.

### Felipe Vergara R - Validación funcional

Ayer:

- Revisó que las historias del sprint representen necesidades reales del producto.
- Apoyó la definición funcional de los criterios de aceptación.

Hoy:

- Validar que el formulario de reporte no tenga campos innecesarios.
- Revisar que la información mostrada en el mapa sea clara para el usuario.
- Confirmar que HU-03 y HU-04 cumplen el objetivo ciudadano del producto.

Bloqueos:

- No registra bloqueos.

### lucasmaulenr - Product Owner

Ayer:

- Revisó el estado del Sprint 1 en Taiga.
- Verificó las historias comprometidas para el sprint.
- Preparó la documentación de la Daily Meeting 2.

Hoy:

- Registrar la Daily Meeting 2 en la wiki del proyecto.
- Confirmar el alcance final antes del cierre del sprint.
- Revisar que las historias pasen de New a In progress cuando comience la implementación.
- Verificar que las tareas técnicas queden asociadas a las HU del Sprint 1.

Bloqueos:

- Falta actualizar el estado de las historias si el equipo ya comenzó la implementación.

## Acuerdos

- El foco del sprint será HU-03 y HU-04.
- Las tareas del Scrum Team se definieron a partir de esas dos historias.
- Frontend y backend deben coordinar el contrato de datos del incidente.
- El equipo debe actualizar los estados de Taiga antes del cierre del sprint.
- No se agregarán nuevas historias al Sprint 1 salvo aprobación del Product Owner.

## Próximos pasos

1. Pasar HU-03 y HU-04 a In progress cuando comience la implementación.
2. Implementar flujo mínimo de reporte de incidente.
3. Implementar visualización básica de incidentes en mapa.
4. Validar cumplimiento de criterios de aceptación.
5. Preparar cierre del Sprint 1 para el 28/04/2026.
