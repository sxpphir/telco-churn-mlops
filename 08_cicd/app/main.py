from pathlib import Path                            # Manejar rutas de archivos

import joblib                                        # Cargar modelo entrenado
import pandas as pd                                  # Crear tabla de entrada
from fastapi import FastAPI                          # Construir API
from fastapi.responses import HTMLResponse           # Devolver la página HTML

from app.schemas import CustomerInput                # Validar datos

ROOT = Path(__file__).resolve().parents[1]           # Carpeta del proyecto

app = FastAPI(title="Telco Churn API")               # Crear aplicación

MODEL_PATH = ROOT / "models" / "champion.joblib"     # Ruta del modelo
model = joblib.load(MODEL_PATH)                      # Cargar pipeline entrenado


@app.get("/", response_class=HTMLResponse)           # Formulario HTML
def home():
    return (ROOT / "templates" / "index.html").read_text(encoding="utf-8")


@app.get("/health")                                  # Endpoint de estado
def health():                                        # Definir función
    return {"status": "ok"}                          # Confirmar funcionamiento


@app.post("/predict")                                # Endpoint de predicción
def predict(customer: CustomerInput):                # Recibir datos validados
    data = pd.DataFrame([customer.model_dump()])     # Convertir a DataFrame
    prediction = int(model.predict(data)[0])         # Predecir clase
    probability = float(model.predict_proba(data)[0, 1])  # Probabilidad de abandono

    if probability < 0.30:                           # Riesgo inferior a 30 %
        risk_level = "Bajo"                          # Asignar nivel bajo
    elif probability < 0.70:                         # Riesgo inferior a 70 %
        risk_level = "Medio"                         # Asignar nivel medio
    else:                                            # Riesgo igual o superior a 70 %
        risk_level = "Alto"                          # Asignar nivel alto

    return {                                         # Devolver respuesta JSON
        "prediction": prediction,                    # Clase estimada
        "churn_probability": probability,            # Probabilidad positiva
        "risk_level": risk_level,                    # Agregar clasificación de riesgo
        "message": (                                 # Mensaje interpretativo
            "Cliente con riesgo de abandono"
            if prediction == 1
            else "Cliente con bajo riesgo de abandono"
        ),
    }