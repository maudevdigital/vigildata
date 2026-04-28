# VigilData - Manual de Instalación

VigilData es una aplicación web para reportar y visualizar incidentes de seguridad ciudadana sobre un mapa interactivo. El objetivo principal es transformar reportes ciudadanos en información útil para conocer zonas de riesgo por comuna, fecha, tipo de incidente y nivel de riesgo.

## Versiones del entorno

| Herramienta | Versión |
|-------------|---------|
| Python | 3.13 |
| Node.js | 20+ |
| npm | 10+ |
| FastAPI | 0.115.0 |
| Vue | 3.5.x |
| Vite | 6.x |
| Supabase | Cloud |

## Requisitos previos

1. Python 3.13+
2. Node.js 20+
3. Cuenta de Supabase
4. Git

## 1. Clonar el repositorio

```bash
git clone https://github.com/maudevdigital/vigildata.git
cd vigildata
```

## 2. Configurar Supabase

1. Crear un proyecto en Supabase.
2. Ir a `Project Settings > Database > Connection string > Session pooler`.
3. Copiar la URI de conexión.
4. Ir a `Project Settings > API Keys` y copiar la `publishable key`.

## 3. Backend

```bash
cd vigildata-backend
python -m venv venv

# Windows PowerShell
.\venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
```

Crear `vigildata-backend/.env`:

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

El backend queda disponible en `http://localhost:8000`.

## 4. Frontend

```bash
cd vigildata-frontend
npm install
```

Crear `vigildata-frontend/.env`:

```env
VITE_SUPABASE_URL=https://xxxxx.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxxx
```

Iniciar el servidor de desarrollo:

```bash
npm run dev
```

El frontend queda disponible en `http://localhost:5173`.

## 5. Credenciales por defecto

| Rol | Email | Contraseña |
|-----|-------|------------|
| ANALISTA | admin@vigildata.cl | admin123 |

## 6. Estructura del proyecto

```text
vigildata/
  README.md
  docs/
  vigildata-backend/
    requirements.txt
    app/
      main.py
      config.py
      database.py
      models/
      schemas/
      routers/
  vigildata-frontend/
    package.json
    src/
      main.js
      App.vue
      router/
      services/
      stores/
      views/
```

## 7. Stack tecnológico

| Capa | Tecnología |
|------|------------|
| Frontend | Vue 3, Vite, Pinia, TailwindCSS |
| Mapa | Leaflet.js, OpenStreetMap |
| Backend | FastAPI, Pydantic, SQLAlchemy |
| Base de datos | Supabase PostgreSQL |
| Autenticación | JWT, bcrypt |
| Cliente HTTP | Axios |

## 8. Endpoints principales

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| GET | `/` | Health check | No |
| POST | `/auth/registro` | Crear cuenta | No |
| POST | `/auth/login` | Obtener token JWT | No |
| GET | `/auth/me` | Obtener usuario autenticado | Sí |
| POST | `/incidentes/` | Crear incidente | Sí |
| GET | `/incidentes/` | Listar incidentes | No |

Filtros disponibles en `GET /incidentes/`:

- `comuna`
- `fecha_inicio`
- `fecha_fin`

## 9. Documentación del proyecto

La documentación formal del proyecto se encuentra en `docs/`.

El documento DOCX principal del proyecto es `VigilData_Arquitectura_4+1_v2.docx`, que consolida la arquitectura y la planificación trabajada en Taiga.
