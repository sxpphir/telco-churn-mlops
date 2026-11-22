from fastapi.testclient import TestClient       # Cliente para probar FastAPI

from app.main import app                        # Importar aplicación

client = TestClient(app)                        # Crear cliente de pruebas

CLIENTE = {                                     # Cliente de ejemplo válido
    "tenure": 5,
    "MonthlyCharges": 85.5,
    "TotalCharges": 427.5,
    "Contract": "Month-to-month",
    "InternetService": "Fiber optic",
}


def test_predict():                             # La predicción responde correctamente
    response = client.post("/predict", json=CLIENTE)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in (0, 1)                  # Clase válida
    assert 0.0 <= data["churn_probability"] <= 1.0       # Probabilidad válida
    assert data["risk_level"] in ("Bajo", "Medio", "Alto")


def test_predict_datos_invalidos():             # Pydantic rechaza datos inválidos
    response = client.post("/predict", json={**CLIENTE, "tenure": -10})
    assert response.status_code == 422


def test_home_html():                           # El formulario HTML se sirve
    response = client.get("/")
    assert response.status_code == 200
    assert "Telco Churn Predictor" in response.text
