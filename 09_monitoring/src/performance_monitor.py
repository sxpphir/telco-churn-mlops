import joblib                                     # Cargar modelo
import pandas as pd                               # Manipular datos
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "Contract", "InternetService"]

model = joblib.load("models/champion.joblib")     # Cargar pipeline completo


def evaluar(ruta):                                # Métricas con etiquetas reales
    df = pd.read_csv(ruta)
    y = (df["Churn"] == "Yes").astype(int)        # 1 = abandono
    pred = model.predict(df[FEATURES])
    prob = model.predict_proba(df[FEATURES])[:, 1]
    return {
        "Accuracy": accuracy_score(y, pred),
        "F1-score": f1_score(y, pred),
        "ROC-AUC": roc_auc_score(y, prob),
    }


ref = evaluar("data/reference.csv")               # Periodo histórico
cur = evaluar("data/current_with_labels.csv")     # Periodo actual con etiquetas reales

print(f"{'Métrica':10s}{'Referencia':>12s}{'Actual':>10s}{'Cambio':>10s}")
for m in ref:
    print(f"{m:10s}{ref[m]:>12.3f}{cur[m]:>10.3f}{cur[m] - ref[m]:>+10.3f}")

# ----- Alerta sencilla (Actividad 7) -----
auc_reference = round(ref["ROC-AUC"], 2)        # ROC-AUC histórica
auc_current = round(cur["ROC-AUC"], 2)          # ROC-AUC actual
# auc_current = 0.82                            # Quitar el # para probar un caso sin deterioro
threshold = 0.10                                # Caída absoluta permitida

print(f"\nROC-AUC referencia: {auc_reference} | actual: {auc_current} | umbral: {threshold}")
if auc_reference - auc_current > threshold:     # Comparar deterioro
    print("ALERTA: revisar rendimiento")        # Mostrar advertencia
else:                                           # Sin deterioro superior al umbral
    print("Rendimiento dentro del umbral")      # Mostrar estado
