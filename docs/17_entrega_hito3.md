# Entrega Hito 3 - VigilData

Documento maestro de la entrega final. Mapea cada criterio de la rúbrica con su
evidencia concreta en el repositorio y el sistema desplegado.

- **Repositorio:** https://github.com/maudevdigital/vigildata
- **Despliegue:** Vercel (frontend + backend) — pestaña *Deployments* en GitHub
- **Base de datos:** PostgreSQL gestionado (Supabase)

---

## 1. Mapeo rúbrica → evidencia

| Criterio (pts) | Evidencia |
|----------------|-----------|
| **Requerimientos y funcionalidades (20)** | HU-01 a HU-11 implementadas y operativas. Ver trazabilidad en `14_arquitectura_final.md` §7 y `02_product_backlog.md`. |
| **Integración del sistema (15)** | Frontend (Vue) ↔ Backend (FastAPI) ↔ BD (Supabase/SQLite) ↔ Supabase Auth (Google) funcionando integrados. Smoke test end-to-end documentado en §3. |
| **Calidad técnica y arquitectura (10)** | Separación routers/services/models/schemas; coherente con el diseño del Hito 1. Ver `14_arquitectura_final.md`. |
| **Pruebas y corrección de errores (15)** | 25 pruebas unitarias (pytest), cobertura ~76%. Bugs corregidos en §4. Ver `10_testing_unitario_cobertura.md` y `15_manual_tecnico.md` §6. |
| **Gestión y trazabilidad (10)** | 34 commits con convención (feat/fix/docs/chore), historias trazadas a Taiga y a commits. Ver §2 y `08_estado_taiga_actual.md`. |
| **Documentación técnica (10)** | Arquitectura final, manual técnico y manual de instalación (`14`–`16`), más README extendido. |
| **Despliegue y operación (5)** | Sistema desplegado en Vercel + Supabase, accesible públicamente. Ver `16_manual_instalacion.md` §5. |
| **Presentación / demo / defensa (15)** | Guion en `13_guion_video_presentacion_solucion.md`; guion de demo en §5 de este documento. |

---

## 2. Historias de usuario entregadas

| HU | Descripción | Sprint | Estado |
|----|-------------|--------|--------|
| HU-01 | Registro de usuario con email | 2 | ✅ Done |
| HU-02 | Inicio de sesión con JWT | 2 | ✅ Done |
| HU-03 | Reportar incidente con GPS | 1 | ✅ Done |
| HU-04 | Ver mapa con incidentes | 1 | ✅ Done |
| HU-05 | Filtrar incidentes por comuna y fecha | 2 | ✅ Done |
| HU-06 | Clasificar incidente por tipo y nivel de riesgo | 3 | ✅ Done |
| HU-07 | Moderar incidentes reportados | 3 | ✅ Done |
| HU-08 | Ver resumen de incidentes por comuna y tipo | 3 | ✅ Done |
| HU-09 | Consolidar denuncias repetidas (similitud BERT) | 3 | ✅ Done |
| HU-10 | Autenticación con Google (Supabase Auth) | 3 | ✅ Done |
| HU-11 | Mejoras de interfaz móvil | 3 | ✅ Done |

> **Trazabilidad Taiga (verificada vía API el 2026-06-19):** las 11 historias
> están en estado *Done* y cerradas; las 30 tareas técnicas, cerradas; los 3
> sprints, cerrados; 0 issues abiertos. El tablero está alineado con el código.

---

## 3. Evidencia de integración (smoke test end-to-end)

Ejecutado al cierre del Hito 3 sobre el backend local (SQLite):

| Paso | Endpoint | Resultado |
|------|----------|-----------|
| Health | `GET /` | `200` `{"status":"ok","proyecto":"VigilData"}` |
| Login admin | `POST /auth/login` | `200` + `access_token` |
| Crear incidente | `POST /incidentes/` (Bearer) | `201` incidente creado |
| Listar | `GET /incidentes/` | `200` incluye el incidente |
| Resumen | `GET /incidentes/resumen` | `200` conteos por comuna/tipo |
| Sin token | `POST /incidentes/` | `403` Not authenticated (autorización OK) |

Frontend: `npm run build` compila sin errores (build de producción verificado).

---

## 4. Pruebas y corrección de errores

- **Suite:** 25 pruebas unitarias con `pytest`, cobertura **~76%** (umbral mínimo
  configurado 60%).
- **Bug corregido en Hito 3:** tres pruebas de `test_incidentes.py` quedaron
  desalineadas tras HU-09/HU-10 (el esquema pasó a exigir `nivel_riesgo` y el
  listado aplica filtros base para ocultar reportes hijos consolidados y
  rechazados). Se actualizaron las pruebas para reflejar el comportamiento real;
  toda la suite quedó en verde.

---

## 5. Guion de demo (defensa técnica)

1. **Contexto** (30s): problema de seguridad ciudadana, propuesta de mapa
   colaborativo.
2. **Reportar** (HU-03): crear un incidente desde el mapa con geolocalización.
3. **Visualizar** (HU-04/05): mapa con marcadores; filtrar por comuna/fecha.
4. **Consolidación inteligente** (HU-09): crear varios reportes similares cercanos
   en el tiempo → se agrupan y, al tercero, se auto-aprueban.
5. **Moderación** (HU-06/07): entrar como analista (`admin@vigildata.cl`),
   aprobar/rechazar, ver `nivel_riesgo`.
6. **Resumen** (HU-08): conteos por comuna y tipo.
7. **Login con Google** (HU-10) y **UI móvil** (HU-11): bottom sheet, FAB.
8. **Cierre técnico**: arquitectura (3 capas, Vercel + Supabase), decisiones
   clave (JWT unificado, BERT con fallback, BD intercambiable).

---

## 6. Índice de documentación para la entrega

| Doc | Contenido |
|-----|-----------|
| `01`–`07`, `09`, `12` | Visión, backlog, sprints, dailies, requisitos, guiones |
| `08` | Estado de Taiga (trazabilidad) |
| `10` | Testing unitario y cobertura |
| `11` | Cierre Sprint 3 |
| `13` | Guion del video de presentación |
| `14` | **Arquitectura final** |
| `15` | **Manual técnico** |
| `16` | **Manual de instalación** |
| `17` | **Este documento (entrega Hito 3)** |
| `README.md` | Manual de instalación extendido |
