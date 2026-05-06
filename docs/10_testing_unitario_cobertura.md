# Taller: Testing Unitario, Mocking y Cobertura de Codigo

## Datos generales

| Campo | Detalle |
|-------|---------|
| Asignatura | Ingenieria de Software 1 |
| Proyecto | VigilData |
| Repositorio | `maudevdigital/vigildata` |
| Fecha de ejecucion | 06/05/2026 |
| Duracion del taller | 90 minutos |
| Backend probado | FastAPI, SQLAlchemy, Pydantic, JWT |
| Herramientas de prueba | `pytest`, `pytest-cov`, `unittest.mock` |

## Contexto del proyecto

VigilData es una aplicacion web para reportar y visualizar incidentes de seguridad ciudadana. El sistema permite registrar usuarios, iniciar sesion, reportar incidentes con ubicacion y consultar incidentes mediante filtros.

Para este taller se reviso el estado del proyecto en GitHub y Taiga:

- GitHub: repositorio `maudevdigital/vigildata`, rama principal `main`.
- Taiga: proyecto `Ingenieria de software 1`, slug `maudevdigital-ingenieria-de-software-1`, ID `1786600`.
- Taiga: HU-01 a HU-05 aparecen cerradas en Sprint 1 y Sprint 2.
- Taiga: HU-06, HU-07 y HU-08 aparecen abiertas en Sprint 3.
- Taiga Wiki: se revisaron las paginas `home`, `vision-y-alcance`, `product-backlog`, `planificacion-sprints`, `requisitos-y-criterios`, `tareas-tecnicas`, `daily-meeting` y `daily-meeting-3-sprint-2-y-pruebas`.

## Objetivo general del taller

Aplicar tecnicas basicas de aseguramiento de calidad mediante pruebas unitarias, mocking de dependencias externas y analisis de cobertura sobre funcionalidades reales del proyecto VigilData.

## Objetivos especificos aplicados

| Objetivo solicitado | Como se cumple en VigilData |
|--------------------|-----------------------------|
| Implementar pruebas unitarias sobre funcionalidades reales | Se agregaron pruebas para registro, login JWT, validacion de token, creacion de incidentes y filtros de incidentes. |
| Utilizar mocking para aislar dependencias externas | Se simulo la base de datos SQLAlchemy, el hashing de contrasena y la generacion de JWT. |
| Ejecutar herramientas de cobertura de codigo | Se configuro `pytest-cov` en `vigildata-backend/pytest.ini`. |
| Analizar la calidad tecnica del codigo probado | Se documentan riesgos cubiertos, errores controlados y beneficios de la cobertura. |

## Modulo o funcionalidad seleccionada

Se selecciono el backend/API de VigilData, especificamente los modulos:

- `vigildata-backend/app/routers/auth.py`
- `vigildata-backend/app/routers/incidentes.py`
- `vigildata-backend/app/schemas/usuario.py`
- `vigildata-backend/app/schemas/incidente.py`

La seleccion se justifica porque estas rutas concentran funcionalidades criticas del sistema:

- Registro de usuarios.
- Inicio de sesion con JWT.
- Validacion de usuario autenticado.
- Registro de incidentes.
- Listado y filtrado de incidentes.

Estas funcionalidades estan relacionadas con historias reales del proyecto:

| Historia Taiga | Funcionalidad relacionada |
|----------------|---------------------------|
| HU-01: Registro de usuario con email | Endpoint `POST /auth/registro` |
| HU-02: Inicio de sesion con JWT | Endpoint `POST /auth/login` y validacion de token |
| HU-03: Reportar incidente con GPS | Endpoint `POST /incidentes/` |
| HU-05: Filtrar incidentes por comuna y fecha | Endpoint `GET /incidentes/` |

## Parte 1: Pruebas unitarias

### Carpeta de tests

Las pruebas se encuentran en:

```text
vigildata-backend/tests/
```

Archivos creados:

```text
vigildata-backend/tests/test_auth.py
vigildata-backend/tests/test_incidentes.py
```

### Requisito minimo

El taller solicita al menos 5 pruebas unitarias. En VigilData se implementaron 12 pruebas unitarias.

| Requisito | Estado |
|----------|--------|
| Minimo 5 pruebas unitarias | Cumplido: 12 pruebas |
| Casos exitosos | Cumplido |
| Casos invalidos | Cumplido |
| Validaciones | Cumplido |
| Manejo de errores o excepciones | Cumplido |

### Detalle de pruebas implementadas

| N | Prueba | Archivo | Tipo de caso | Que valida |
|---|--------|---------|--------------|------------|
| 1 | `test_registro_crea_usuario_con_password_hasheada` | `test_auth.py` | Exitoso | El registro crea un usuario, hashea la contrasena y confirma la transaccion. |
| 2 | `test_registro_rechaza_email_duplicado` | `test_auth.py` | Invalido/error | Si el email ya existe, retorna error HTTP 400 y no guarda el usuario. |
| 3 | `test_login_exitoso_emite_token_y_usuario` | `test_auth.py` | Exitoso | El login verifica la contrasena y emite un token JWT. |
| 4 | `test_login_rechaza_credenciales_invalidas` | `test_auth.py` | Invalido/error | Si el usuario no existe o la clave es incorrecta, retorna HTTP 401. |
| 5 | `test_obtener_usuario_actual_decodifica_token_y_busca_usuario` | `test_auth.py` | Exitoso | Un token valido permite obtener el usuario autenticado. |
| 6 | `test_obtener_usuario_actual_rechaza_token_invalido` | `test_auth.py` | Invalido/error | Un token corrupto o mal formado retorna HTTP 401. |
| 7 | `test_obtener_usuario_actual_rechaza_usuario_inexistente` | `test_auth.py` | Invalido/error | Un token valido con usuario inexistente retorna HTTP 401. |
| 8 | `test_usuario_create_valida_formato_email` | `test_auth.py` | Validacion | Pydantic rechaza emails con formato incorrecto. |
| 9 | `test_crear_incidente_persiste_usuario_autenticado` | `test_incidentes.py` | Exitoso | La creacion de incidente asocia el reporte al usuario autenticado. |
| 10 | `test_listar_incidentes_sin_filtros_ordena_por_fecha_descendente` | `test_incidentes.py` | Exitoso | El listado general ordena incidentes por fecha descendente. |
| 11 | `test_listar_incidentes_aplica_filtros_de_comuna_y_fechas` | `test_incidentes.py` | Validacion | El endpoint aplica filtros por comuna, fecha de inicio y fecha de fin. |
| 12 | Parametrizacion de credenciales invalidas | `test_auth.py` | Invalido/error | Se prueban dos variantes: usuario inexistente y password incorrecta. |

### Casos validos identificados

Los principales casos validos fueron:

- Registrar un usuario nuevo con email valido.
- Iniciar sesion con email y contrasena correctos.
- Decodificar un token JWT valido y recuperar el usuario.
- Crear un incidente con usuario autenticado.
- Listar incidentes sin filtros.
- Listar incidentes filtrando por comuna y rango de fechas.

### Casos invalidos identificados

Los principales casos invalidos fueron:

- Intentar registrar un email ya existente.
- Iniciar sesion con usuario inexistente.
- Iniciar sesion con contrasena incorrecta.
- Enviar un token invalido.
- Enviar un token valido asociado a un usuario que ya no existe.
- Crear un usuario con email mal formado.

### Manejo de errores o excepciones

Las pruebas validan los siguientes errores:

| Error probado | Respuesta esperada |
|---------------|--------------------|
| Email duplicado | `HTTPException` con estado `400` |
| Credenciales invalidas | `HTTPException` con estado `401` |
| Token invalido | `HTTPException` con estado `401` |
| Usuario no encontrado | `HTTPException` con estado `401` |
| Email mal formado | `ValidationError` de Pydantic |

## Parte 2: Mocking

### Dependencias externas simuladas

El taller solicita simular al menos una dependencia externa. En VigilData se simularon varias:

| Dependencia | Por que se mockea | Como se mockea |
|-------------|-------------------|----------------|
| Base de datos SQLAlchemy | Para no depender de Supabase/PostgreSQL real durante las pruebas | `MagicMock` para `db.query`, `filter`, `first`, `add`, `commit`, `refresh`, `order_by` y `all` |
| Hash de contraseña | Para no ejecutar bcrypt real en cada prueba y controlar el resultado | `patch.object(auth.pwd_context, "hash")` |
| Verificacion de contraseña | Para probar login exitoso e invalido sin depender de hashes reales | `patch.object(auth.pwd_context, "verify")` |
| Generacion de token JWT | Para aislar la prueba de login y verificar solo que se solicita emitir token | `patch.object(auth, "crear_token")` |

### Ejemplo de mocking usado

En las pruebas se simula la cadena de consulta de SQLAlchemy:

```python
query = MagicMock()
query.filter.return_value = query
query.first.return_value = usuario_mock

db = MagicMock()
db.query.return_value = query
```

Esto permite probar codigo que normalmente haria:

```python
db.query(Usuario).filter(Usuario.email == usuario.email).first()
```

sin conectarse a una base de datos real.

### Beneficio del mocking en este taller

Gracias al mocking, las pruebas:

- Se ejecutan de forma aislada.
- No requieren Supabase.
- No modifican datos reales.
- Son rapidas y repetibles.
- Permiten forzar escenarios dificiles de reproducir manualmente, como token invalido o usuario inexistente.

## Parte 3: Cobertura de codigo

### Herramienta usada

Se uso `pytest-cov`, configurado en:

```text
vigildata-backend/pytest.ini
```

Configuracion aplicada:

```ini
[pytest]
testpaths = tests
pythonpath = .
addopts = --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=60
```

Esto significa que cada vez que se ejecuta `pytest`, tambien se ejecuta el analisis de cobertura.

### Comandos de ejecucion

Desde la carpeta del backend:

```bash
cd vigildata-backend
pip install -r requirements.txt
python -m pytest
```

Tambien se puede ejecutar explicitamente:

```bash
python -m pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=60
```

### Resultado obtenido

Resultado de ejecucion del 06/05/2026:

```text
12 passed, 2 warnings
TOTAL: 194 statements, 34 missed, 82.47% coverage
Required test coverage of 60% reached.
```

### Cumplimiento del requisito de cobertura

| Requisito | Resultado |
|----------|-----------|
| Cobertura minima solicitada | 60% |
| Cobertura obtenida | 82.47% |
| Estado | Cumplido |

### Resumen de cobertura por archivo

| Archivo | Cobertura |
|---------|-----------|
| `app/routers/auth.py` | 98% |
| `app/routers/incidentes.py` | 100% |
| `app/schemas/usuario.py` | 100% |
| `app/schemas/incidente.py` | 100% |
| `app/models/usuario.py` | 100% |
| `app/models/incidente.py` | 100% |
| Total del backend medido | 82.47% |

El archivo con reporte HTML se genera en:

```text
vigildata-backend/htmlcov/index.html
```

Ese archivo puede abrirse en el navegador para tomar la captura solicitada por el profesor.

## Entregables

### 1. Codigo fuente actualizado con carpeta de tests

Archivos agregados o modificados:

```text
vigildata-backend/tests/test_auth.py
vigildata-backend/tests/test_incidentes.py
vigildata-backend/pytest.ini
vigildata-backend/requirements.txt
.gitignore
```

### 2. Evidencia de ejecucion de pruebas

Comando ejecutado:

```bash
python -m pytest
```

Resultado:

```text
12 passed, 2 warnings
```

### 3. Captura o reporte de cobertura

Reporte en terminal:

```text
TOTAL: 194 statements, 34 missed, 82.47% coverage
Required test coverage of 60% reached.
```

Reporte HTML:

```text
vigildata-backend/htmlcov/index.html
```

### 4. Breve reflexion tecnica

La reflexion tecnica se incluye en la siguiente seccion.

## Reflexion tecnica

### Que errores detectaron mediante testing?

Las pruebas permitieron detectar y dejar controlados errores esperados en funcionalidades criticas del backend:

- Registro con email duplicado.
- Inicio de sesion con credenciales invalidas.
- Token JWT invalido o corrupto.
- Token valido asociado a un usuario inexistente.
- Email con formato incorrecto.

Tambien se verifico que los flujos exitosos funcionen correctamente:

- Registro crea usuario y hashea contrasena.
- Login exitoso emite token.
- Usuario autenticado puede ser obtenido desde un token valido.
- Incidente creado queda asociado al usuario autenticado.
- Filtros de incidentes se aplican correctamente.

No se encontro un bug productivo nuevo durante la ejecucion, pero las pruebas dejan protegidos los casos donde el sistema debe responder con errores controlados en vez de fallar de forma inesperada.

### Que dificultad tuvieron al implementar mocking?

La principal dificultad fue simular correctamente la cadena de consultas de SQLAlchemy, porque el codigo usa llamadas encadenadas como:

```python
db.query(Usuario).filter(Usuario.email == usuario.email).first()
```

y:

```python
db.query(Incidente).filter(...).order_by(...).all()
```

Para resolverlo se usaron objetos `MagicMock` que devuelven el mismo objeto de consulta despues de cada `filter`. Esto permite probar la logica sin crear una base de datos real ni insertar datos de prueba en Supabase.

Otra dificultad fue aislar el login, ya que normalmente depende de bcrypt y JWT. Se soluciono usando `patch.object` sobre `pwd_context.verify`, `pwd_context.hash` y `crear_token`.

### Que beneficios aporta la cobertura de codigo?

La cobertura de codigo permite medir que partes del backend fueron ejecutadas durante las pruebas. En este taller ayudo a comprobar que las funcionalidades criticas de autenticacion e incidentes quedaron cubiertas por pruebas automatizadas.

Los beneficios principales son:

- Reduce el riesgo de regresiones al modificar login, registro o filtros.
- Permite identificar archivos o funciones sin pruebas suficientes.
- Entrega evidencia objetiva para el profesor y para el equipo.
- Facilita mantener el proyecto en futuros sprints.
- Da confianza para refactorizar codigo sin romper comportamientos esperados.

La cobertura no garantiza que no existan errores, pero si entrega una medida concreta de cuanto codigo fue ejercitado por pruebas y ayuda a mejorar la calidad tecnica del proyecto.

## Conclusion

El taller fue aplicado sobre funcionalidades reales de VigilData. Se implementaron 12 pruebas unitarias, se uso mocking para aislar dependencias externas y se obtuvo una cobertura total de 82.47%, superando el minimo solicitado de 60%.

Con esto se cumplen los entregables solicitados:

- Codigo fuente actualizado con carpeta de tests.
- Evidencia de ejecucion de pruebas.
- Reporte de cobertura.
- Reflexion tecnica sobre errores, mocking y cobertura.
