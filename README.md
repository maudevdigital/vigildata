# VigilData — Manual de instalacion (Sprint 3 / Hito 2)

VigilData es una aplicacion web para reportar y visualizar incidentes de
seguridad ciudadana sobre un mapa interactivo.

Este README es la guia oficial para que el equipo deje el proyecto listo
para grabar el video del **Hito 2**. Incluye las mejoras incorporadas en el
Sprint 3 a partir del review del profesor:

- **HU-09**: control de repeticion de denuncias con BERT — si llegan mas de
  3 reportes similares dentro de 30 minutos y a menos de 200 m, el sistema
  los consolida automaticamente.
- **HU-10**: autenticacion con Google a traves de **Supabase Auth**.
- **HU-11**: mejoras de interfaz movil (bottom sheet de filtros, FAB,
  cards en admin, safe-area iOS).

---

## Tabla de contenidos

1. [Stack y versiones](#1-stack-y-versiones)
2. [Estructura del proyecto](#2-estructura-del-proyecto)
3. [Clonar el repositorio](#3-clonar-el-repositorio)
4. [Eleccion de base de datos](#4-eleccion-de-base-de-datos)
5. [Backend — setup paso a paso](#5-backend--setup-paso-a-paso)
6. [Frontend — setup paso a paso](#6-frontend--setup-paso-a-paso)
7. [Configurar Supabase Auth con Google (HU-10)](#7-configurar-supabase-auth-con-google-hu-10)
8. [Migracion HU-09 / HU-10 en la base de datos](#8-migracion-hu-09--hu-10-en-la-base-de-datos)
9. [Arrancar la aplicacion](#9-arrancar-la-aplicacion)
10. [Smoke test end-to-end para el video](#10-smoke-test-end-to-end-para-el-video)
11. [Pruebas automatizadas](#11-pruebas-automatizadas)
12. [Endpoints de la API](#12-endpoints-de-la-api)
13. [Variables de entorno (resumen)](#13-variables-de-entorno-resumen)
14. [Troubleshooting](#14-troubleshooting)

---

## 1. Stack y versiones

| Herramienta | Version |
|-------------|---------|
| Python | 3.13 |
| Node.js | 20+ |
| npm | 10+ |
| FastAPI | 0.115 |
| Vue | 3.5 |
| Vite | 6.x |
| Pinia | 3.x |
| TailwindCSS | 3.x |
| Leaflet | 1.9 |
| Supabase | Auth + Postgres (opcional como BD) |
| sentence-transformers | 3.0.1 (HU-09, opcional — hay fallback) |

---

## 2. Estructura del proyecto

```
vigildata/
  README.md
  docs/evidencia/
    hu09/  hu10/  hu11/       # capturas y bitacoras del Sprint 3
  vigildata-backend/
    app/
      main.py
      config.py
      database.py
      models/        usuario.py, incidente.py
      schemas/       usuario.py, incidente.py
      routers/       auth.py, auth_google.py, incidentes.py
      services/      duplicados_bert.py, google_oauth.py
    tests/
      test_auth.py
      test_auth_google.py         # HU-10
      test_duplicados_bert.py     # HU-09
      test_incidentes.py
    alter_db_hu09_hu10.py
    requirements.txt
  vigildata-frontend/
    src/
      main.js
      App.vue
      router/
      services/      api.js, googleAuth.js
      stores/        authStore.js, incidentesStore.js
      components/    IncidenteResumen.vue, BottomSheet.vue   # HU-11
      assets/        mobile.css                              # HU-11
      views/         HomeView, LoginView, RegistroView, MapaView, ReportarView, AdminView
```

---

## 3. Clonar el repositorio

```powershell
git clone https://github.com/maudevdigital/vigildata.git
cd vigildata
git checkout main
```

Todo el trabajo del Sprint 3 vive en la rama `main`.

---

## 4. Eleccion de base de datos

Hay dos opciones soportadas, definidas por la variable `DATABASE_URL` en
`vigildata-backend/.env`:

### Opcion A — SQLite local (recomendada para grabar el video)

- No requiere red ni credenciales.
- La BD se crea automaticamente en `vigildata-backend/local-demo.db` al
  primer arranque.
- Es la opcion activa por defecto:

  ```env
  DATABASE_URL=sqlite:///./local-demo.db
  ```

### Opcion B — Supabase Postgres (produccion)

1. En Supabase Dashboard del proyecto: **Project Settings → Database →
   Connection string → URI**.
2. Reemplazar `<password>` por la contrasena del usuario `postgres`
   (Project Settings → Database → "Reset database password" si la perdiste).
3. Pegar en `vigildata-backend/.env`:

   ```env
   DATABASE_URL=postgresql://postgres.mdcualtcxwlxsivemkmf:<password>@aws-1-us-west-2.pooler.supabase.com:5432/postgres?sslmode=require
   ```

> Importante: Supabase **Auth** se usa siempre (HU-10), independiente de si
> la BD es SQLite o Supabase Postgres. La BD solo afecta donde se guardan
> `usuarios`, `incidentes`, etc.

---

## 5. Backend — setup paso a paso

### 5.1 Crear venv e instalar dependencias

```powershell
cd vigildata-backend
python -m venv venv
.\venv\Scripts\Activate.ps1
# si Windows bloquea, ejecutar primero en la misma terminal:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

pip install -r requirements.txt
```

`requirements.txt` ya incluye `sentence-transformers` para HU-09 (la
descarga del modelo BERT es la primera vez ~120 MB; si no hay internet, el
servicio cae a un embedding hashing deterministico — los tests funcionan
igual).

### 5.2 Crear .env

Copiar `vigildata-backend/.env.example` a `vigildata-backend/.env` y editar:

```env
# Base de datos (Opcion A o B de la seccion 4)
DATABASE_URL=sqlite:///./local-demo.db

# JWT propio del backend (cambiar en produccion)
SECRET_KEY=dev-secret-key-vigildata-2026
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# HU-10 — Supabase Auth para validar el access_token de Google
SUPABASE_URL=https://mdcualtcxwlxsivemkmf.supabase.co
# (opcional) Fallback si Supabase aun usa HS256:
# SUPABASE_JWT_SECRET=
```

---

## 6. Frontend — setup paso a paso

### 6.1 Instalar dependencias

```powershell
cd vigildata-frontend
npm install
```

### 6.2 Crear .env

Copiar `vigildata-frontend/.env.example` a `vigildata-frontend/.env`:

```env
VITE_SUPABASE_URL=https://mdcualtcxwlxsivemkmf.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxxx
```

La `PUBLISHABLE_KEY` (anon) se saca de Supabase Dashboard → Project
Settings → API → "Publishable and secret API keys" → "Publishable key" →
copiar el valor que empieza con `sb_publishable_`.

> **NUNCA** pegar la Secret key (`sb_secret_*`) en el frontend.

---

## 7. Configurar Supabase Auth con Google (HU-10)

Estos pasos solo se hacen una vez por proyecto. Si ya estan hechos en
`mdcualtcxwlxsivemkmf`, podes saltar a la seccion 9.

### 7.1 Crear OAuth client en Google Cloud Console

1. Ingresar a https://console.cloud.google.com/apis/credentials.
2. "Create credentials" → "OAuth client ID" → Application type: "Web application".
3. Authorized JavaScript origins:
   ```
   http://localhost:5173
   ```
4. Authorized redirect URIs:
   ```
   https://mdcualtcxwlxsivemkmf.supabase.co/auth/v1/callback
   ```
5. Crear y copiar **Client ID** y **Client Secret**.
6. En "OAuth consent screen" → seccion **Test users**, agregar los emails
   de quienes vayan a probar (PO, Benja, Seba, profesor).

### 7.2 Habilitar el provider en Supabase

1. Supabase Dashboard → Authentication → **Sign In / Providers** → Google → Enable.
2. Pegar Client ID y Client Secret obtenidos en 7.1. Guardar.

### 7.3 URLs de redireccion

1. Supabase Dashboard → Authentication → **URL Configuration**:
   - Site URL: `http://localhost:5173`
   - Redirect URLs: agregar `http://localhost:5173/login`

### 7.4 Verificar JWT signing key

El backend descarga la clave publica automaticamente desde:

```
https://mdcualtcxwlxsivemkmf.supabase.co/auth/v1/.well-known/jwks.json
```

No hace falta copiar ningun secret. Lo unico necesario en el backend es
`SUPABASE_URL`.

---

## 8. Migracion HU-09 / HU-10 en la base de datos

Sprint 3 agrega columnas nuevas:

- `incidentes.incidente_raiz_id` (FK opcional para consolidar reportes).
- `incidentes.reportes_asociados` (INT default 1).
- `usuarios.provider` (VARCHAR default 'local').

Ejecutar la migracion idempotente:

```powershell
cd vigildata-backend
.\venv\Scripts\Activate.ps1
python alter_db_hu09_hu10.py
```

Compatible con SQLite y Postgres. No falla si las columnas ya existen.

---

## 9. Arrancar la aplicacion

### 9.1 Terminal 1 — Backend

```powershell
cd vigildata-backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Queda en http://localhost:8000. El admin seed
(`admin@vigildata.cl` / `admin123`) se crea automaticamente al primer
arranque.

### 9.2 Terminal 2 — Frontend

```powershell
cd vigildata-frontend
npm run dev
```

Queda en http://localhost:5173.

---

## 10. Smoke test end-to-end para el video

Antes de grabar, correr este recorrido y verificar que todo funcione:

### 10.1 Login como ANALISTA

1. http://localhost:5173/login
2. Email `admin@vigildata.cl`, password `admin123`.
3. Debe redirigir a `/admin` y mostrar el panel.

### 10.2 Login como CIUDADANO via Google (HU-10)

1. Logout, volver a `/login`.
2. Click en "Continuar con Google".
3. Aceptar el consent screen (debe ser un email agregado como Test User en
   Google Cloud Console).
4. Debe redirigir a `/mapa`, autenticado como CIUDADANO.
5. Verificar en Supabase Dashboard → Authentication → Users que aparece
   el usuario nuevo, y en VigilData → /admin (con admin seed) que aparece
   tambien en la tabla `usuarios` con `provider='supabase-google'`.

### 10.3 Reportar incidente (HU-06)

1. Como CIUDADANO en `/mapa`, click sobre el mapa.
2. Llenar tipo, nivel de riesgo, descripcion.
3. Submit. Debe aparecer un marcador con el color del nivel.

### 10.4 Auto-aprobacion por similitud (HU-09)

1. Crear 4 incidentes en menos de 30 minutos, todos en la misma comuna,
   coordenadas casi identicas, descripcion similar (por ejemplo "robo de
   bicicleta en la plaza principal" cuatro veces).
2. Los primeros 1-2 quedaran `pendiente` (esperan moderacion).
3. Al llegar al **3er** reporte equivalente, el incidente raiz y el nuevo
   se marcan `aprobado` automaticamente. El campo `auto_aprobado=true`
   aparece en la respuesta del POST.
4. Verificable con la query en la BD:
   ```sql
   SELECT id, estado, incidente_raiz_id, reportes_asociados
   FROM incidentes ORDER BY id DESC;
   ```

### 10.5 Moderar incidentes (HU-07)

1. Logueado como ANALISTA en `/admin`.
2. Aprobar o rechazar incidentes pendientes; verificar que el mapa publico
   esconde los rechazados.

### 10.6 Resumen por comuna y tipo (HU-08)

1. En `/mapa`, panel "Filtrar incidentes" + componente `IncidenteResumen`.
2. Aplicar filtros (region, comuna, fecha, nivel de riesgo) y confirmar
   que los conteos del resumen y los marcadores del mapa coinciden.

### 10.7 Mejoras moviles (HU-11)

1. En Chrome DevTools, activar "Device toolbar" y elegir perfil iPhone 12
   (390x844) o 360x780.
2. Verificar en `/mapa`:
   - Mapa ocupa la pantalla, sin scroll horizontal.
   - Boton "Filtros" arriba a la derecha abre el **Bottom Sheet**.
   - FAB "+" abajo a la derecha abre el modal de reporte.
3. Verificar en `/reportar`: formulario en una columna, submit accesible
   con el teclado abierto.
4. Verificar en `/admin`: incidentes pendientes se muestran como **cards**
   con tres botones grandes (Aprobar / Rechazar / Borrar) en lugar de
   tabla.

### 10.8 Capturas para el video / evidencia

Dejar las capturas en:

- `docs/evidencia/hu09/` — 4to reporte auto-aprobado + salida pytest.
- `docs/evidencia/hu10/` — boton Google, redirect, pytest.
- `docs/evidencia/hu11/` — capturas 360x780 de cada vista.

---

## 11. Pruebas automatizadas

Suite Sprint 3:

```powershell
cd vigildata-backend
.\venv\Scripts\Activate.ps1
pytest tests/test_duplicados_bert.py tests/test_auth_google.py -v --no-cov
```

Resultado esperado: **10 passed**.

- 7 casos HU-09 (similitud coseno, haversine, ventana 30 min, auto-aprobacion).
- 3 casos HU-10 (usuario nuevo, vinculacion, 401).

Para correr toda la suite con cobertura:

```powershell
pytest --cov=app --cov-report=term-missing
```

> Hay 4 tests heredados (`test_incidentes.py`, `test_api.py`) que fallan
> por motivos previos al Sprint 3 (faltaba `nivel_riesgo` en payloads de
> prueba). No se tocan por scope. La cobertura del codigo nuevo de Sprint
> 3 es >= 90%.

---

## 12. Endpoints de la API

| Metodo | Ruta | Descripcion | Auth |
|--------|------|-------------|------|
| GET | `/` | Health check | No |
| POST | `/auth/registro` | Crear cuenta local | No |
| POST | `/auth/login` | Login email/password — devuelve JWT propio | No |
| POST | `/auth/google` | **HU-10** — Recibe `{id_token}` de Supabase, devuelve JWT propio | No |
| GET | `/auth/me` | Devuelve el usuario autenticado | Si |
| POST | `/incidentes/` | Crear incidente. **HU-09** aplica consolidacion automatica | Si |
| GET | `/incidentes/` | Listar (filtros: region, comuna, nivel_riesgo, estado, fecha_inicio, fecha_fin) | No |
| GET | `/incidentes/resumen` | **HU-08** — totales por comuna y por tipo | No |
| PATCH | `/incidentes/{id}/estado` | **HU-07** — moderacion (solo ANALISTA) | Si |
| DELETE | `/incidentes/{id}` | Eliminar (solo ANALISTA) | Si |

---

## 13. Variables de entorno (resumen)

### Backend (`vigildata-backend/.env`)

| Variable | Obligatoria | Descripcion |
|----------|-------------|-------------|
| `DATABASE_URL` | Si | SQLite o Postgres (ver seccion 4) |
| `SECRET_KEY` | Si | Firma del JWT propio del backend |
| `ALGORITHM` | Si | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Si | `60` |
| `SUPABASE_URL` | Si (HU-10) | URL base del proyecto Supabase |
| `SUPABASE_JWT_SECRET` | No | Fallback HS256 para tokens legacy |
| `HU09_VENTANA_MIN` | No | Ventana temporal en minutos (default 30) |
| `HU09_DISTANCIA_MAX_M` | No | Distancia max en metros (default 200) |
| `HU09_UMBRAL_SIMILITUD` | No | Umbral similitud coseno (default 0.85) |
| `HU09_AUTO_APROBAR_DESDE` | No | Cantidad de reportes para auto-aprobar (default 3) |
| `HU09_MODELO` | No | Modelo sentence-transformers (default `paraphrase-multilingual-MiniLM-L12-v2`) |

### Frontend (`vigildata-frontend/.env`)

| Variable | Obligatoria | Descripcion |
|----------|-------------|-------------|
| `VITE_SUPABASE_URL` | Si | URL del proyecto Supabase |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | Si | Publishable (anon) key |

---

## 14. Troubleshooting

**Login con Google devuelve "Access blocked"**
- Falta agregar el email como "Test user" en Google Cloud Console → OAuth consent screen.

**Frontend muestra "Falta VITE_SUPABASE_URL en .env"**
- Vite no recargo el `.env`. Detener `npm run dev` (Ctrl+C) y volver a iniciar.

**Backend devuelve 500 "SUPABASE_URL no esta configurado"**
- Falta la variable en `vigildata-backend/.env`. Setear y reiniciar uvicorn.

**Backend devuelve 401 "id_token invalido"**
- El token expiro (Supabase emite tokens con expiracion corta). Hacer logout en el frontend (`localStorage.clear()`) y volver a entrar.

**Backend devuelve 401 al reportar incidente despues de un rato**
- El JWT propio del backend dura 60 min. Volver a loguear.

**`alter_db_hu09_hu10.py` no agrega columnas**
- Es idempotente: ya estaban. Confirmar con `PRAGMA table_info(incidentes);` en SQLite o `\d incidentes` en psql.

**Modelo BERT no descarga (sin internet)**
- El servicio cae automaticamente a un embedding hashing deterministico.
  Los tests pasan igual; la deteccion es algo menos semantica pero
  funciona para la demo.

**Mapa no muestra marcadores**
- Verificar que el incidente este `aprobado` (los `rechazado` se filtran
  por defecto). Usar `?estado=todos` en el GET para depurar.

---

## Equipo del Sprint 3

- **lucasmaulenr** — Product Owner / coordinacion
- **benjaosan** — Frontend (HU-08, HU-11, frontend de HU-10)
- **SebaNG** — Backend (HU-06, HU-07, HU-09, backend de HU-10)
- **Felipe Vergara R** — Scrum Master / apoyo funcional
