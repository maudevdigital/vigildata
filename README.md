# VigilData — Manual de Instalación

## Versiones del entorno

| Herramienta | Versión  |
|-------------|----------|
| Python      | 3.13     |
| Node.js     | 20+      |
| npm         | 10+      |
| FastAPI     | 0.115.0  |
| Vue         | 3.5.x    |
| Vite        | 6.x      |
| Supabase    | Cloud    |

---

## Requisitos previos

1. **Python 3.13+** — [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **Node.js 20+** — [https://nodejs.org/](https://nodejs.org/)
3. **Cuenta Supabase** — [https://supabase.com/](https://supabase.com/)
4. **Git** — [https://git-scm.com/](https://git-scm.com/)

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/maudevdigital/vigildata.git
cd vigildata
```

---

## 2. Configurar Supabase

1. Crear un proyecto en [supabase.com](https://supabase.com)
2. Ir a **Project Settings → Database → Connection string → Session pooler**
3. Copiar la URI (formato: `postgresql://postgres.xxxxx:[PASSWORD]@aws-x-region.pooler.supabase.com:5432/postgres`)
4. Ir a **Project Settings → API Keys** y copiar la `publishable key` y la `secret key`

---

## 3. Backend (FastAPI)

```bash
cd vigildata-backend
python -m venv venv

# Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Crear el archivo `.env` en `vigildata-backend/`:

```env
DATABASE_URL=postgresql://postgres.xxxxx:[PASSWORD]@aws-x-region.pooler.supabase.com:5432/postgres?sslmode=require
SECRET_KEY=una-clave-secreta-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Ejecutar el servidor:

```bash
uvicorn app.main:app --reload
```

El backend levanta en **http://localhost:8000** y crea las tablas automáticamente en Supabase al iniciar, junto con el usuario admin por defecto.

---

## 4. Frontend (Vue 3)

```bash
cd vigildata-frontend
npm install
```

Crear el archivo `.env` en `vigildata-frontend/`:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxxx
```

Iniciar el servidor de desarrollo:

```bash
npm run dev
```

El frontend levanta en **http://localhost:5173**

---

## 5. Credenciales por defecto

| Rol      | Email                  | Contraseña |
|----------|------------------------|------------|
| ANALISTA | admin@vigildata.cl     | admin123   |

---

## 6. Estructura del proyecto

```
vigildata/
├── README.md
│
├── vigildata-backend/          # API REST (FastAPI)
│   ├── .env                    # Variables de entorno (no subir al repo)
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # Punto de entrada + seed admin
│       ├── config.py           # Variables de entorno
│       ├── database.py         # Conexión a Supabase (psycopg)
│       ├── models/             # Modelos SQLAlchemy
│       │   ├── usuario.py      # Rol: CIUDADANO / ANALISTA
│       │   └── incidente.py
│       ├── schemas/            # DTOs Pydantic
│       │   ├── usuario.py
│       │   └── incidente.py
│       └── routers/            # Endpoints REST
│           ├── auth.py         # /auth/registro, /auth/login, /auth/me
│           └── incidentes.py   # /incidentes (CRUD)
│
└── vigildata-frontend/         # SPA (Vue 3)
    ├── .env                    # Variables de entorno (no subir al repo)
    ├── vite.config.js
    ├── tailwind.config.js
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue             # Navbar dinámica según rol
        ├── router/index.js     # Guards de autenticación y rol
        ├── services/api.js     # Cliente Axios
        ├── utils/supabase.ts   # Cliente Supabase JS
        ├── stores/
        │   ├── authStore.js    # Estado de autenticación (Pinia)
        │   └── incidentesStore.js
        └── views/
            ├── HomeView.vue
            ├── LoginView.vue
            ├── RegistroView.vue
            ├── MapaView.vue
            ├── ReportarView.vue
            └── AdminView.vue   # Solo ANALISTA
```

---

## 7. Stack tecnológico

| Capa          | Tecnología                         | Versión   |
|---------------|------------------------------------|-----------|
| Frontend      | Vue 3 + Vite + Pinia + TailwindCSS | 3.5 / 6.x |
| Mapa          | Leaflet.js + OpenStreetMap         | 1.9.4     |
| Backend       | FastAPI + Pydantic + SQLAlchemy    | 0.115.0   |
| Base de datos | Supabase (PostgreSQL 16)           | Cloud     |
| Autenticación | JWT (python-jose) + bcrypt         | HS256     |
| HTTP Client   | Axios                              | 1.7.7     |
| Supabase JS   | @supabase/supabase-js              | 2.x       |

---

## 8. Endpoints de la API

| Método | Ruta              | Descripción           | Auth     |
|--------|-------------------|-----------------------|----------|
| GET    | /                 | Health check          | No       |
| POST   | /auth/registro    | Crear cuenta          | No       |
| POST   | /auth/login       | Obtener token JWT     | No       |
| GET    | /auth/me          | Datos del usuario     | Sí       |
| POST   | /incidentes/      | Crear incidente       | Sí       |
| GET    | /incidentes/      | Listar incidentes     | No       |

Documentación interactiva: **http://localhost:8000/docs**

**Filtros disponibles en GET /incidentes/:**
- `?comuna=Santiago`
- `?fecha_inicio=2026-01-01T00:00:00`
- `?fecha_fin=2026-12-31T23:59:59`

---

## 9. Solución de problemas

| Problema | Solución |
|----------|----------|
| `getaddrinfo failed` en backend | Usar Session Pooler de Supabase (no la URL directa). |
| Error `bcrypt` al iniciar | Ejecutar `pip install bcrypt==4.0.1` en el venv. |
| CORS error en navegador | Verificar que backend corra en `localhost:8000` y frontend en `localhost:5173`. |
| 401 en login | Verificar que el hash de la contraseña en la BD sea de bcrypt 4.x. |
| Leaflet no muestra mapa | Verificar conexión a internet (tiles desde OpenStreetMap). |

---

## 4. Estructura del proyecto

```
vigildata/
├── docker-compose.yml          # Orquestación de servicios
├── README.md
│
├── vigildata-backend/          # API REST (FastAPI)
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── .env.example
│   ├── requirements.txt
│   └── app/
│       ├── main.py             # Punto de entrada
│       ├── config.py           # Variables de entorno
│       ├── database.py         # Conexión a PostgreSQL
│       ├── models/             # Modelos SQLAlchemy
│       │   ├── usuario.py
│       │   └── incidente.py
│       ├── schemas/            # DTOs Pydantic
│       │   ├── usuario.py
│       │   └── incidente.py
│       └── routers/            # Endpoints REST
│           ├── auth.py         # /auth/registro, /auth/login
│           └── incidentes.py   # /incidentes (CRUD)
│
└── vigildata-frontend/         # SPA (Vue 3)
    ├── Dockerfile
    ├── .dockerignore
    ├── vite.config.js
    ├── tailwind.config.js
    ├── package.json
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── services/api.js     # Cliente Axios
        ├── stores/
        │   ├── authStore.js
        │   └── incidentesStore.js
        └── views/
            ├── HomeView.vue
            ├── LoginView.vue
            ├── RegistroView.vue
            ├── MapaView.vue
            └── ReportarView.vue
```

---

## 5. Stack tecnológico

| Capa          | Tecnología                          | Versión    |
|---------------|-------------------------------------|------------|
| Frontend      | Vue 3 + Vite + Pinia + TailwindCSS  | 3.5 / 6.x  |
| Mapa          | Leaflet.js + OpenStreetMap          | 1.9.4      |
| Backend       | FastAPI + Pydantic + SQLAlchemy     | 0.115.0    |
| Base de datos | PostgreSQL (Docker)                 | 16         |
| Autenticación | JWT (python-jose) + bcrypt          | HS256      |
| HTTP Client   | Axios                               | 1.7.7      |
| Contenedores  | Docker + Docker Compose             | 26+        |

---

## 6. Endpoints de la API

| Método | Ruta               | Descripción          | Auth |
|--------|--------------------|----------------------|------|
| GET    | /                  | Health check         | No   |
| POST   | /auth/registro     | Crear cuenta         | No   |
| POST   | /auth/login        | Obtener token JWT    | No   |
| POST   | /incidentes/       | Crear incidente      | Sí   |
| GET    | /incidentes/       | Listar incidentes    | No   |

Documentación interactiva: **http://localhost:8000/docs**

**Filtros disponibles en GET /incidentes/:**
- `?comuna=Santiago`
- `?fecha_inicio=2026-01-01T00:00:00`
- `?fecha_fin=2026-12-31T23:59:59`

---

## 7. Solución de problemas

| Problema | Solución |
|----------|----------|
| `docker-compose up` falla | Asegúrate de que Docker Desktop esté corriendo. |
| Puerto 5432 en uso | Detén el PostgreSQL local o cambia el puerto en `docker-compose.yml`. |
| CORS error en el navegador | Verifica que el backend corra en `localhost:8000` y el frontend en `localhost:5173`. |
| Error de conexión a BD | Espera a que el healthcheck de `db` pase. El backend depende de él. |
| Leaflet no muestra mapa | Verifica conexión a internet (los tiles se cargan desde OpenStreetMap). |
