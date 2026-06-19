# Arquitectura final - VigilData (Hito 3)

Documento de arquitectura consolidado del sistema tal como quedó al cierre del
Hito 3. Complementa el documento `VigilData_Arquitectura_4+1_v2.docx` (vista 4+1
formal) con el estado real del código desplegado.

---

## 1. Visión general

VigilData es una aplicación web de **mapa colaborativo de seguridad ciudadana**:
los habitantes reportan incidentes (con geolocalización) y los visualizan en
tiempo real sobre un mapa interactivo. Un rol analista modera los reportes y
consulta resúmenes agregados.

Arquitectura **cliente-servidor en tres capas**, desplegada como dos servicios
independientes (frontend SPA + backend API REST) sobre una base de datos
gestionada.

```
┌──────────────────────┐      HTTPS / JSON      ┌──────────────────────┐
│   Frontend (SPA)     │  ───────────────────►  │   Backend (API REST) │
│   Vue 3 + Vite       │  ◄───────────────────  │   FastAPI (Python)   │
│   Leaflet (mapa)     │      JWT Bearer        │   SQLAlchemy ORM     │
│   Pinia (estado)     │                        │   BERT (HU-09)       │
└──────────┬───────────┘                        └──────────┬───────────┘
           │                                               │
           │ Supabase JS (OAuth Google, HU-10)             │ SQL
           ▼                                               ▼
┌──────────────────────┐                        ┌──────────────────────┐
│   Supabase Auth      │                        │  PostgreSQL (Supabase)│
│   (Google provider)  │                        │  / SQLite (local-demo)│
└──────────────────────┘                        └──────────────────────┘
```

---

## 2. Stack tecnológico

| Capa | Tecnología | Versión | Rol |
|------|-----------|---------|-----|
| Frontend | Vue 3 + Vite | 3.5 / 6.0 | SPA, vistas y routing |
| Frontend | Leaflet | 1.9 | Mapa interactivo y marcadores |
| Frontend | Pinia | 2.2 | Estado global (auth, incidentes) |
| Frontend | Tailwind CSS | 3.4 | Estilos / UI móvil (HU-11) |
| Frontend | @supabase/supabase-js | 2.x | Login con Google (HU-10) |
| Backend | FastAPI | 0.115 | API REST + validación |
| Backend | SQLAlchemy | 2.0 | ORM y acceso a datos |
| Backend | python-jose | 3.3 | Emisión/validación de JWT propio |
| Backend | passlib + bcrypt | 1.7 / 3.2 | Hash de contraseñas |
| Backend | sentence-transformers | (opcional) | Similitud semántica BERT (HU-09) |
| Datos | PostgreSQL (Supabase) | — | Persistencia en producción |
| Datos | SQLite | — | Fallback local para demo/tests |
| Deploy | Vercel | — | Hosting de frontend y backend |

---

## 3. Vista de componentes

### 3.1 Backend (`vigildata-backend/app`)

```
app/
├── main.py            # FastAPI app, CORS, lifespan (crea tablas + seed admin)
├── config.py          # Lee y sanea variables de entorno
├── database.py        # Engine SQLAlchemy + sesión + Base declarativa
├── models/            # Entidades ORM: Usuario, Incidente
├── schemas/           # Esquemas Pydantic (entrada/salida)
├── routers/           # Endpoints: auth, auth_google, incidentes
└── services/          # Lógica de dominio: duplicados_bert (HU-09), google_oauth (HU-10)
```

Separación por responsabilidades: **routers** (HTTP) → **services** (dominio) →
**models** (persistencia), con **schemas** como contrato de la API. Esta
modularidad es coherente con el diseño definido en el Hito 1.

### 3.2 Frontend (`vigildata-frontend/src`)

```
src/
├── router/index.js        # Rutas + guards (requiereAuth, soloAdmin)
├── stores/                # Pinia: authStore, incidentesStore
├── services/              # api.js (axios + interceptores), googleAuth.js, geocoding.js
├── views/                 # HomeView, LoginView, RegistroView, MapaView, ReportarView, AdminView
├── components/            # BottomSheet, IncidenteResumen
└── utils/                 # regiones.js, supabase.ts
```

`api.js` centraliza la URL base, inyecta el token JWT en cada request y, ante un
`401`, limpia la sesión y redirige a `/login` (interceptor de respuesta).

---

## 4. Modelo de datos

### Tabla `usuarios`
| Campo | Tipo | Notas |
|-------|------|-------|
| id | int PK | |
| email | str único | |
| password | str | hash bcrypt |
| rol | enum | `CIUDADANO` \| `ANALISTA` |
| provider | str | `local` \| `supabase-google` |

### Tabla `incidentes`
| Campo | Tipo | Notas |
|-------|------|-------|
| id | int PK | |
| tipo | str | categoría del incidente |
| descripcion | str | texto libre (insumo de BERT) |
| fecha | datetime | UTC, default ahora |
| latitud / longitud | float | geolocalización |
| region / comuna | str | ubicación administrativa |
| nivel_riesgo | str | bajo/medio/alto |
| estado | str | `pendiente` \| `aprobado` \| `rechazado` |
| usuario_id | FK usuarios | autor del reporte |
| revisado_por_id | FK usuarios | analista que moderó |
| fecha_revision | datetime | |
| incidente_raiz_id | FK incidentes | **HU-09**: apunta a la denuncia raíz si es repetición |
| reportes_asociados | int | **HU-09**: nº de reportes consolidados bajo la raíz |

La auto-referencia `incidente_raiz_id` permite **consolidar denuncias repetidas**
sin perder el conteo (HU-09).

---

## 5. Decisiones de arquitectura clave

1. **JWT propio + Supabase para Google (HU-10).** El backend emite su propio JWT
   (`/auth/login`, `/auth/registro`). Para Google, el frontend usa Supabase Auth
   y el backend valida el `id_token` y emite un JWT del mismo formato
   (`/auth/google`). Esto unifica la autorización: todos los endpoints protegidos
   validan **un solo tipo de token**.

2. **Detección de duplicados con degradación elegante (HU-09).** El servicio
   `duplicados_bert` usa `sentence-transformers` (BERT multilingüe) cuando está
   disponible; si no (CI, sin internet, o bundle serverless de Vercel), cae a un
   *embedding por hashing determinista*. Reglas de consolidación: misma comuna,
   ≤ 200 m, ventana de 30 min y similitud coseno ≥ 0.85. Al acumular ≥ 3 reportes
   se auto-aprueba. Todos los umbrales son configurables por variable de entorno.

3. **Base de datos intercambiable.** `DATABASE_URL` decide PostgreSQL (Supabase,
   producción) o SQLite (`local-demo.db`, demo/tests). El mismo código corre en
   ambos motores; SQLite garantiza una demo sin dependencias de red.

4. **Saneo de variables de entorno.** `config.py` recorta BOM/espacios/saltos de
   línea de los valores de entorno para evitar fallos al cargar `.env` desde
   PowerShell en Windows.

5. **Despliegue serverless.** Backend y frontend se despliegan por separado en
   Vercel; las dependencias pesadas de ML viven en `requirements-dev.txt` y NO se
   instalan en producción, manteniendo el bundle dentro del límite serverless.

---

## 6. Vista de despliegue

| Componente | Entorno | URL (producción) |
|------------|---------|------------------|
| Frontend (SPA) | Vercel | `https://vigildata-frontend.vercel.app` |
| Backend (API) | Vercel | `https://vigildata-backend.vercel.app` |
| Base de datos | Supabase (PostgreSQL gestionado) | `mdcualtcxwlxsivemkmf.supabase.co` |
| Auth Google | Supabase Auth | provider Google habilitado |

> Ambos dominios de producción son públicos (el backend responde en `/` y expone
> la documentación interactiva en `/docs`). Para desarrollo local: frontend
> `http://localhost:5173`, backend `http://localhost:8000`.

---

## 7. Trazabilidad arquitectura ↔ historias de usuario

| HU | Componente backend | Componente frontend |
|----|--------------------|---------------------|
| HU-01 Registro email | `routers/auth.py` (`/auth/registro`) | RegistroView |
| HU-02 Login JWT | `routers/auth.py` (`/auth/login`, `obtener_usuario_actual`) | LoginView, authStore |
| HU-03 Reportar con GPS | `routers/incidentes.py` (POST) | ReportarView, geocoding.js |
| HU-04 Ver mapa | `routers/incidentes.py` (GET) | MapaView (Leaflet) |
| HU-05 Filtrar | `_aplicar_filtros` | MapaView, incidentesStore |
| HU-06/07 Clasificar/Moderar | `nivel_riesgo`, `estado`, PATCH `/estado`, DELETE | AdminView |
| HU-08 Resumen | `/incidentes/resumen` | IncidenteResumen |
| HU-09 Consolidar repetidos | `services/duplicados_bert.py` | conteo agrupado en mapa |
| HU-10 Login Google | `routers/auth_google.py`, `services/google_oauth.py` | googleAuth.js, supabase.ts |
| HU-11 UI móvil | — | BottomSheet, mobile.css, FAB |
