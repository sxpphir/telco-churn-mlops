import joblib                                     # Cargar modelo
import pandas as pd                               # Manipular datos

FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "Contract", "InternetService"]

model = joblib.load("models/champion.joblib")     # Cargar pipeline completo

reference = pd.read_csv("data/reference.csv")     # Datos históricos
current = pd.read_csv("data/current.csv")         # Datos nuevos

reference["prediction"] = (                       # Predicción histórica
    model.predict_proba(reference[FEATURES])[:, 1]   # Probabilidad de abandono
)
current["prediction"] = (                         # Predicción actual
    model.predict_proba(current[FEATURES])[:, 1]     # Probabilidad de abandono
)

print("=== Probabilidad de abandono: REFERENCIA ===")
print(reference["prediction"].describe().round(3))    # Resumen histórico
print("\n=== Probabilidad de abandono: ACTUAL ===")
print(current["prediction"].describe().round(3))      # Resumen actual

print("\n=== % de clientes clasificados como abandono (probabilidad >= 0.5) ===")
print(f"Referencia: {(reference['prediction'] >= 0.5).mean():.1%}")
print(f"Actual:     {(current['prediction'] >= 0.5).mean():.1%}")
