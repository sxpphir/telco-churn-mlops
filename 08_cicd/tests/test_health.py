from fastapi.testclient import TestClient       # Cliente para probar FastAPI

from app.main import app                        # Importar aplicación

client = TestClient(app)                        # Crear cliente de pruebas


def test_health():                              # Definir prueba
    response = client.get("/health")            # Consultar endpoint
    assert response.status_code == 200
    assert response.json()["status"] == "ok"    # Verificar contenido
