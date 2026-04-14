# VigilData — Manual de Instalación

## Versiones del entorno

| Herramienta         | Versión   |
|---------------------|-----------|
| Python              | 3.13.12   |
| Node.js             | 22.15.0   |
| npm                 | 11.5.2    |
| FastAPI             | 0.115.0   |
| Vue                 | 3.5.x     |
| Vite                | 6.x       |
| PostgreSQL (Supabase)| 15+      |

---

## Requisitos previos

1. **Python 3.12+** — [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. **Node.js 20+** — [https://nodejs.org/](https://nodejs.org/)
3. **Git** — [https://git-scm.com/](https://git-scm.com/)
4. **Cuenta en Supabase** (gratuita) — [https://supabase.com/](https://supabase.com/) para la base de datos PostgreSQL.

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/<tu-usuario>/vigildata.git
cd vigildata
```

---

## 2. Configurar el Backend (FastAPI)

### 2.1 Crear entorno virtual e instalar dependencias

```bash
cd vigildata-backend
python -m venv venv
```

**Activar el entorno virtual:**

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

**Instalar dependencias:**

```bash
pip install -r requirements.txt
```

### 2.2 Configurar variables de entorno

Copiar el archivo de ejemplo y editarlo con tus credenciales de Supabase:

```bash
cp .env.example .env
```

Editar `.env`:

```env
DATABASE_URL=postgresql://postgres.<ref>:<password>@aws-0-us-east-1.pooler.supabase.com:6543/postgres
SECRET_KEY=una-clave-secreta-segura-de-al-menos-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> La URL de conexión se obtiene desde **Supabase → Project Settings → Database → Connection string (URI)**.

### 2.3 Ejecutar el servidor de desarrollo

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:
- **http://localhost:8000** — Raíz
- **http://localhost:8000/docs** — Documentación Swagger automática

### 2.4 Verificar que funciona

```bash
curl http://localhost:8000/
# Respuesta esperada: {"status":"ok","proyecto":"VigilData"}
```

---

## 3. Configurar el Frontend (Vue 3)

### 3.1 Instalar dependencias

```bash
cd vigildata-frontend
npm install
```

### 3.2 Ejecutar el servidor de desarrollo

```bash
npm run dev
```

La aplicación estará disponible en **http://localhost:5173**.

### 3.3 Build de producción

```bash
npm run build
```

Los archivos estáticos se generan en `dist/`.

---

## 4. Estructura del proyecto

```
vigildata/
├── vigildata-backend/          # API REST (FastAPI)
│   ├── app/
│   │   ├── main.py             # Punto de entrada de la API
│   │   ├── config.py           # Variables de entorno
│   │   ├── database.py         # Conexión a PostgreSQL
│   │   ├── models/             # Modelos SQLAlchemy
│   │   │   ├── usuario.py
│   │   │   └── incidente.py
│   │   ├── schemas/            # DTOs Pydantic
│   │   │   ├── usuario.py
│   │   │   └── incidente.py
│   │   └── routers/            # Endpoints REST
│   │       ├── auth.py         # /auth/registro, /auth/login
│   │       └── incidentes.py   # /incidentes (CRUD)
│   ├── requirements.txt
│   └── .env.example
│
├── vigildata-frontend/         # SPA (Vue 3)
│   ├── src/
│   │   ├── main.js             # Punto de entrada
│   │   ├── App.vue             # Layout principal
│   │   ├── router/index.js     # Rutas
│   │   ├── stores/             # Pinia stores
│   │   │   ├── authStore.js
│   │   │   └── incidentesStore.js
│   │   ├── services/api.js     # Cliente Axios
│   │   └── views/              # Vistas
│   │       ├── HomeView.vue
│   │       ├── LoginView.vue
│   │       ├── RegistroView.vue
│   │       ├── MapaView.vue
│   │       └── ReportarView.vue
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
└── README.md
```

---

## 5. Stack tecnológico

| Capa          | Tecnología                         | Versión     |
|---------------|------------------------------------|-------------|
| Frontend      | Vue 3 + Vite + Pinia + TailwindCSS| 3.5 / 6.x  |
| Mapa          | Leaflet.js + OpenStreetMap         | 1.9.4       |
| Backend       | FastAPI + Pydantic + SQLAlchemy    | 0.115.0     |
| Base de datos | PostgreSQL (Supabase)              | 15+         |
| Autenticación | JWT (python-jose) + bcrypt         | HS256       |
| HTTP Client   | Axios                              | 1.7.7       |
| Despliegue    | Vercel + Render + Supabase         | —           |

---

## 6. Endpoints de la API

| Método | Ruta              | Descripción            | Auth |
|--------|--------------------|------------------------|------|
| GET    | /                  | Health check           | No   |
| POST   | /auth/registro     | Crear cuenta           | No   |
| POST   | /auth/login        | Obtener token JWT      | No   |
| POST   | /incidentes/       | Crear incidente        | Sí   |
| GET    | /incidentes/       | Listar incidentes      | No   |

**Filtros disponibles en GET /incidentes/:**
- `?comuna=Santiago`
- `?fecha_inicio=2026-01-01T00:00:00`
- `?fecha_fin=2026-12-31T23:59:59`

---

## 7. Solución de problemas

| Problema | Solución |
|----------|----------|
| `pip install` falla con psycopg | Asegúrate de usar Python 3.12+. El proyecto usa `psycopg[binary]` (psycopg3). |
| CORS error en el navegador | Verifica que el backend corra en `localhost:8000` y el frontend en `localhost:5173`. |
| Error de conexión a BD | Revisa `DATABASE_URL` en `.env` y que tu proyecto Supabase esté activo. |
| Leaflet no muestra mapa | Verifica conexión a internet (los tiles se cargan desde OpenStreetMap). |
