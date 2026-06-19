# Manual técnico - VigilData (Hito 3)

Referencia para desarrolladores: estructura del proyecto, API REST, servicios de
dominio, autenticación y variables de entorno. Para instalar/levantar el sistema
ver `16_manual_instalacion.md` y el `README.md` raíz.

---

## 1. Estructura del repositorio

```
vigildata/
├── vigildata-backend/      # API FastAPI (Python)
│   ├── app/                # código de la aplicación (ver Arquitectura, §3.1)
│   ├── tests/              # pruebas unitarias (pytest)
│   ├── index.py            # entrypoint serverless (Vercel)
│   ├── requirements.txt    # deps de producción
│   ├── requirements-dev.txt# deps de tests + ML (BERT) + migraciones
│   └── vercel.json
├── vigildata-frontend/     # SPA Vue 3 + Vite
│   ├── src/                # código (ver Arquitectura, §3.2)
│   └── vercel.json
└── docs/                   # documentación del proyecto
```

---

## 2. API REST

Base URL local: `http://localhost:8000`. Todos los cuerpos son JSON.
Documentación interactiva autogenerada por FastAPI en `/docs` (Swagger UI).

### 2.1 Autenticación

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/auth/registro` | — | Crea usuario (email+password), devuelve JWT |
| POST | `/auth/login` | — | Valida credenciales, devuelve JWT |
| POST | `/auth/google` | — | Recibe `id_token` de Google (vía Supabase), devuelve JWT propio |
| GET | `/auth/me` | Bearer | Devuelve el usuario autenticado |

**Formato del token** (respuesta de login/registro/google):
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "usuario": { "id": 1, "email": "...", "rol": "ANALISTA" }
}
```
El JWT lleva claims `sub` (id), `email`, `rol`, `exp`. Se envía en cada request
protegida como `Authorization: Bearer <jwt>`.

### 2.2 Incidentes

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/incidentes/` | Bearer | Crea incidente; ejecuta detección de duplicados (HU-09) |
| GET | `/incidentes/` | — | Lista incidentes (oculta hijos consolidados y rechazados) |
| GET | `/incidentes/resumen` | — | Conteos agregados por comuna y por tipo (HU-08) |
| PATCH | `/incidentes/{id}/estado` | Bearer (ANALISTA) | Cambia estado: pendiente/aprobado/rechazado |
| DELETE | `/incidentes/{id}` | Bearer (ANALISTA) | Elimina incidente |

**Filtros de query** (en `GET /incidentes/` y `/resumen`):
`region`, `comuna`, `nivel_riesgo`, `estado`, `fecha_inicio`, `fecha_fin`.
- Sin `estado` se excluyen los `rechazado`.
- `estado=todos` no filtra por estado; `estado=pendiente` incluye también nulos.
- Siempre se ocultan los incidentes hijos (`incidente_raiz_id` no nulo).

**Ejemplo — crear incidente:**
```bash
curl -X POST http://localhost:8000/incidentes/ \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"tipo":"Robo","descripcion":"Robo de bicicleta","latitud":-33.45,
       "longitud":-70.66,"comuna":"Santiago","nivel_riesgo":"alto"}'
```

Códigos relevantes: `201` creado, `401` token inválido/ausente,
`403` sin permisos (rol), `400` validación, `404` no encontrado.

---

## 3. Servicios de dominio

### 3.1 `duplicados_bert` (HU-09)

Detecta y consolida denuncias repetidas. Flujo en `crear_incidente`:
1. Se persiste el incidente (`flush`).
2. `encontrar_duplicado()` busca una raíz candidata según reglas.
3. Si la hay, `aplicar_consolidacion()` enlaza el nuevo a la raíz e incrementa
   `reportes_asociados`; al llegar a `AUTO_APROBAR_DESDE` auto-aprueba.

**Reglas y umbrales (configurables por entorno):**

| Variable | Default | Significado |
|----------|---------|-------------|
| `HU09_VENTANA_MIN` | 30 | Ventana temporal en minutos |
| `HU09_DISTANCIA_MAX_M` | 200 | Distancia máxima (Haversine) en metros |
| `HU09_UMBRAL_SIMILITUD` | 0.85 | Similitud coseno mínima entre descripciones |
| `HU09_AUTO_APROBAR_DESDE` | 3 | Reportes para auto-aprobación |
| `HU09_MODELO` | `paraphrase-multilingual-MiniLM-L12-v2` | Modelo BERT |

**Embeddings:** usa `sentence-transformers` si está instalado; si no, cae a un
*hashing trick* determinista (`_embedding_hashing`). Esto permite correr en CI y
en el bundle serverless de Vercel sin las dependencias pesadas de ML.

### 3.2 `google_oauth` (HU-10)

Valida el `id_token` de Google emitido vía Supabase Auth y extrae el email.
`POST /auth/google` crea el usuario si no existe (rol `CIUDADANO`,
`provider="supabase-google"`) o vincula una cuenta `local` existente, y devuelve
un JWT propio del backend.

---

## 4. Autenticación y autorización

- **Contraseñas:** hash bcrypt (`passlib`).
- **Tokens:** JWT HS256 firmados con `SECRET_KEY`, expiración
  `ACCESS_TOKEN_EXPIRE_MINUTES` (default 60).
- **Dependencia `obtener_usuario_actual`:** decodifica el Bearer, carga el
  usuario y lo inyecta en los endpoints protegidos.
- **Roles:** `CIUDADANO` (reporta) y `ANALISTA` (modera/elimina). Los endpoints
  de moderación verifican `rol == ANALISTA`.
- **Frontend:** guards de Vue Router (`requiereAuth`, `soloAdmin`) + interceptor
  axios que ante `401` limpia sesión y redirige a `/login`.

Admin seed automático al arrancar: `admin@vigildata.cl` / `admin123` (rol
ANALISTA). **Cambiar en cualquier entorno real.**

---

## 5. Variables de entorno

### Backend (`vigildata-backend/.env`)
| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `DATABASE_URL` | Sí | `sqlite:///./local-demo.db` o `postgresql://…` (Supabase) |
| `SECRET_KEY` | Sí | Secreto de firma JWT |
| `ALGORITHM` | No | Default `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Default `60` |
| `SUPABASE_URL` | Sí (HU-10) | URL base del proyecto Supabase |
| `CORS_ORIGINS` | No | Orígenes extra separados por coma (producción) |
| `CORS_ORIGIN_REGEX` | No | Regex de orígenes permitidos |
| `HU09_*` | No | Umbrales de detección de duplicados (§3.1) |

### Frontend (`vigildata-frontend/.env`)
| Variable | Requerida | Descripción |
|----------|-----------|-------------|
| `VITE_SUPABASE_URL` | Sí | URL del proyecto Supabase |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | Sí | Anon/publishable key de Supabase |
| `VITE_API_URL` | Sí (prod) | URL base del backend |

---

## 6. Pruebas

Suite con `pytest` en `vigildata-backend/tests/`:

| Archivo | Cubre |
|---------|-------|
| `test_auth.py` | Registro, login, validación de token |
| `test_auth_google.py` | Login con Google (HU-10) |
| `test_incidentes.py` | Crear/listar/filtrar incidentes |
| `test_duplicados_bert.py` | Similitud, Haversine y consolidación (HU-09) |
| `test_api.py` | Smoke de endpoints |

Ejecutar:
```bash
cd vigildata-backend
./venv/Scripts/activate        # Windows
pytest                          # corre con cobertura (umbral mínimo 60%)
```
Estado al cierre del Hito 3: **25 pruebas, todas en verde, cobertura ~76%**.
Reporte HTML de cobertura en `vigildata-backend/htmlcov/index.html`.
