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