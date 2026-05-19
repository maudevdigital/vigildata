## 0. Configurar la base de datos (primera vez)

Copiar `vigildata-backend/.env.example` a `vigildata-backend/.env` y elegir UNA opción:

- **Opción A (Supabase):** descomentar la línea `DATABASE_URL=postgresql://...` y poner las credenciales reales del proyecto Supabase.
- **Opción B (SQLite local):** dejar `DATABASE_URL=sqlite:///./local-demo.db`. No requiere red ni credenciales; se usa para la demo si Supabase no está disponible.

El admin seed (`admin@vigildata.cl` / `admin123`) se crea automáticamente en cualquiera de las dos.

---

1. Encender el Backend (La API)
Abre tu carpeta vigildata en Visual Studio Code.

Ve a Terminal > New Terminal.

Entra a la carpeta del backend:
cd vigildata-backend

Aplica el permiso temporal que acordamos para que Windows no te bloquee:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Activa tu entorno virtual (debería aparecer el texto verde (venv)):


.\venv\Scripts\activate

Arranca el servidor:
uvicorn app.main:app --reload
(¡Y listo! Deja esa terminal tranquila y no la cierres).

2. Encender el Frontend (La Página Web)
Haz clic en el ícono de "+" (arriba a la derecha en el panel de tu terminal) para abrir una segunda pestaña.

Entra a la carpeta del frontend:
cd vigildata-frontend

Aplica el permiso temporal que acordamos para que Windows no te bloquee:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Arranca la interfaz visual:
npm run dev