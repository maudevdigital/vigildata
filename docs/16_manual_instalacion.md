# Manual de instalación - VigilData (Hito 3)

Guía verificada para levantar VigilData en local. El `README.md` raíz contiene la
versión extendida (configuración de Supabase, Google OAuth, troubleshooting);
este documento resume el camino rápido **probado al cierre del Hito 3**.

## Requisitos previos
- Python 3.11+ (probado en 3.13)
- Node.js 18+ y npm
- Git

## 1. Clonar el repositorio
```bash
git clone https://github.com/maudevdigital/vigildata.git
cd vigildata
```

## 2. Backend (API)
```bash
cd vigildata-backend
python -m venv venv
# Windows (PowerShell):
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt
# (opcional) pruebas + BERT real:  pip install -r requirements-dev.txt
```

Configurar la base de datos: copiar `.env.example` a `.env` y elegir UNA opción:
- **SQLite (demo, sin red, recomendado para evaluar):**
  `DATABASE_URL=sqlite:///./local-demo.db`
- **Supabase (producción):**
  `DATABASE_URL=postgresql://postgres.<proyecto>:<password>@<host>:5432/postgres?sslmode=require`

Definir además `SECRET_KEY` (cualquier cadena para local).

Arrancar:
```bash
uvicorn app.main:app --reload
```
Queda en `http://localhost:8000` (Swagger en `/docs`). Al primer arranque se
crean las tablas y el **admin seed**: `admin@vigildata.cl` / `admin123`.

## 3. Frontend (SPA)
En otra terminal:
```bash
cd vigildata-frontend
npm install
cp .env.example .env     # completar VITE_SUPABASE_URL y VITE_SUPABASE_PUBLISHABLE_KEY
npm run dev
```
Queda en `http://localhost:5173`.

> Para login con Google (HU-10) hay que configurar el provider Google en
> Supabase y las Redirect URLs. El login por email/contraseña funciona sin esa
> configuración. Ver README §7.

## 4. Verificación rápida (smoke test)
Con el backend corriendo:
```bash
# login admin
curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vigildata.cl","password":"admin123"}'
# debe devolver access_token + usuario
```
Pruebas automatizadas:
```bash
cd vigildata-backend && pytest      # 25 pruebas, cobertura ~76%
```

## 5. Despliegue (producción)
Frontend y backend están desplegados en **Vercel** (ver pestaña *Deployments* del
repositorio en GitHub). El backend usa `index.py` + `vercel.json`
(`@vercel/python`); el frontend se construye con `npm run build` → `dist/`.
La base de datos productiva es PostgreSQL gestionado por Supabase.
