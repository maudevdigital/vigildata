# Visión y alcance del producto

## Nombre del proyecto

VigilData.

## Visión

VigilData es un mapa colaborativo de seguridad ciudadana que permite a los habitantes de una comuna reportar incidentes en su entorno y visualizarlos en tiempo real sobre un mapa interactivo.

La idea central es convertir el conocimiento del barrio en datos útiles, sin formularios complicados ni infraestructura pesada.

## Problema

Los ciudadanos suelen conocer eventos de riesgo en su entorno cercano, pero esa información queda dispersa en conversaciones, redes sociales o grupos privados. Esto dificulta que otros vecinos puedan anticiparse, comprender zonas de riesgo o tomar decisiones informadas.

## Objetivo principal

Permitir que los ciudadanos reporten incidentes con ubicación geográfica y que otros usuarios puedan visualizarlos, filtrarlos y comprenderlos en un mapa interactivo.

## Usuarios principales

| Usuario | Necesidad |
|---------|-----------|
| Ciudadano | Reportar incidentes y consultar zonas de riesgo cercanas. |
| Usuario autenticado | Crear reportes válidos asociados a una cuenta. |
| Moderador o analista | Revisar reportes, mejorar calidad de datos y observar patrones. |

## Alcance funcional

El alcance funcional priorizado para el proyecto incluye:

- Registro de usuarios.
- Inicio de sesión con JWT.
- Reporte de incidentes con ubicación GPS.
- Visualización de incidentes en mapa interactivo.
- Filtros por comuna y fecha.
- Clasificación por tipo y nivel de riesgo.
- Moderación de incidentes.
- Resumen de incidentes por comuna y tipo.

## Fuera de alcance inicial

- Aplicación móvil nativa.
- Alertas automáticas en tiempo real.
- Integración con instituciones externas.
- Modelos predictivos de riesgo.
- Geocodificación avanzada.

## Criterio de éxito

El proyecto se considera exitoso si permite completar el flujo mínimo:

1. Un usuario se registra e inicia sesión.
2. El usuario reporta un incidente con ubicación.
3. El incidente se almacena correctamente.
4. Otros ciudadanos pueden visualizarlo en el mapa.
5. Los reportes pueden filtrarse y resumirse para obtener información útil.
