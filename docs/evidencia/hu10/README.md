# Evidencia HU-10 — Autenticacion con Google (via Supabase Auth)

Responsable: SebaNG (backend) y benjaosan (frontend).

Decision de diseno: se usa **Supabase Auth** como proveedor del sign-in con
Google. El frontend llama `supabase.auth.signInWithOAuth({provider:'google'})`
y, al volver del callback, obtiene un `access_token` JWT firmado por Supabase
(HS256 con `SUPABASE_JWT_SECRET`). El backend valida ese token y emite su
propio JWT de aplicacion para autorizar `/incidentes/*` (mismo flujo que
`/auth/login`).

Ventaja: cero servicios extra, ya que VigilData usa Supabase como BD. Un solo
JWT secret a manejar en el backend.

## Codigo

Backend:
- `vigildata-backend/app/services/google_oauth.py` (valida JWT de Supabase con python-jose)
- `vigildata-backend/app/routers/auth_google.py` (`POST /auth/google`)
- `vigildata-backend/app/models/usuario.py` (`provider='supabase-google'`)
- `vigildata-backend/.env.example` (`SUPABASE_JWT_SECRET`)

Frontend:
- `vigildata-frontend/src/services/googleAuth.js` (supabase-js signInWithOAuth)
- `vigildata-frontend/src/stores/authStore.js` (`loginConGoogle`)
- `vigildata-frontend/src/views/LoginView.vue` (boton "Continuar con Google")
- `vigildata-frontend/.env.example` (`VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`)

## Pruebas

Archivo: `vigildata-backend/tests/test_auth_google.py`

```bash
cd vigildata-backend
pytest -v tests/test_auth_google.py
```

Casos (3/3 PASSED):
- `test_google_login_crea_usuario_ciudadano_nuevo` — claims tipo Supabase
  (`aud=authenticated`, `app_metadata.provider=google`) crean usuario CIUDADANO con `provider='supabase-google'`.
- `test_google_login_vincula_cuenta_existente` — segundo login con mismo email no duplica.
- `test_google_login_id_token_invalido_devuelve_401`.

## Configuracion

1. Supabase dashboard > Authentication > Providers > **Google**: enable.
2. En Google Cloud Console crear OAuth client (Web), pegar el Client ID y Client Secret en el provider de Supabase.
3. En Google Cloud Console agregar como Authorized redirect URI:
   `https://<PROJECT>.supabase.co/auth/v1/callback`.
4. Supabase > Authentication > URL Configuration:
   - Site URL: `http://localhost:5173`
   - Redirect URLs: `http://localhost:5173/login`
5. Frontend `.env`: `VITE_SUPABASE_URL`, `VITE_SUPABASE_PUBLISHABLE_KEY`.
6. Backend `.env`: `SUPABASE_JWT_SECRET` (Project settings > API > JWT Secret).

## Caja negra manual

| Caso | Esperado | Resultado |
|------|----------|-----------|
| Click "Continuar con Google" | Redirect a Google, vuelve con sesion Supabase, backend devuelve JWT propio, redirige a `/mapa` | OK |
| Login con mismo email ya existente en BD | Vincula, no duplica usuario | OK |
| Token mal formado en POST /auth/google | 401 | OK |
| Backend sin `SUPABASE_JWT_SECRET` | 500 con mensaje claro | OK |

## Capturas

- `login-supabase-google.png` (LoginView con boton)
- `redirect-google.png` (consent screen)
- `pytest-auth-google.png` (3/3 PASSED)
