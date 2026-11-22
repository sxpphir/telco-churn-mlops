# Práctica 9 — Monitoreo con Evidently AI (Telco Customer Churn)

- `data/reference.csv`: datos históricos (los del entrenamiento del modelo).
- `data/current.csv`: datos nuevos **simulados** de un periodo posterior (sin etiquetas).
- `data/current_with_labels.csv`: los mismos datos nuevos con la etiqueta real `Churn`.
- `models/champion.joblib`: modelo Champion (Regresión Logística).

## Instalar (CMD)
```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

## Ejecutar
```bat
python src/generate_report.py
python src/prediction_monitor.py
python src/performance_monitor.py
```
Abre `reports\data_drift.html` en el navegador.
