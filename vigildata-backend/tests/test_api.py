from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# --- PRUEBA 1: Health Check (Ruta pública) ---
def test_api_funcionando():
    response = client.get("/")
    assert response.status_code == 200

# --- PRUEBA 2: Seguridad al crear incidente (Caja Negra) ---
def test_crear_incidente_sin_token_da_error():
    # Simulamos intentar crear un incidente sin haber iniciado sesión
    response = client.post("/incidentes/", json={"tipo": "Robo", "descripcion": "Test"})
    
    # El sistema debe bloquearnos por no tener autorización (401 o 403)
    assert response.status_code in [401, 403]

# --- PRUEBA 3: Listar incidentes (Ruta pública) ---
def test_listar_incidentes_publicos():
    # Según su manual, GET /incidentes/ no requiere Auth
    response = client.get("/incidentes/")
    
    # El sistema debe dejarnos ver la lista sin problemas
    assert response.status_code == 200