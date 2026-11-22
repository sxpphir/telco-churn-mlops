# Práctica 6 — FastAPI + HTML (Telco Customer Churn)

Modelo incluido: `models/champion.joblib` (Regresión Logística, Champion de la práctica 4),
un pipeline de scikit-learn con preprocesamiento + clasificador, entrenado con:
`tenure`, `MonthlyCharges`, `TotalCharges`, `Contract`, `InternetService`.

## Instalar (CMD)
```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

## Ejecutar
```bat
python -m uvicorn app.main:app --reload
```
- Formulario: http://127.0.0.1:8000/
- Documentación: http://127.0.0.1:8000/docs
- Salud: http://127.0.0.1:8000/health

## Ejemplo para POST /predict
```json
{
  "tenure": 5,
  "MonthlyCharges": 85.5,
  "TotalCharges": 427.5,
  "Contract": "Month-to-month",
  "InternetService": "Fiber optic"
}
```
