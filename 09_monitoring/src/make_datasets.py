"""Genera los datasets de monitoreo (ya incluidos en data/; no es necesario ejecutarlo).

- reference.csv: datos históricos con los que se entrenó el modelo (dataset Telco de las prácticas).
- current.csv: datos nuevos SIMULADOS de un periodo posterior, con cambios intencionales:
  clientes más nuevos, cargos mensuales más altos y más contratos mes a mes.
  InternetService se mantiene estable para comparar.
- current_with_labels.csv: los mismos datos nuevos con la etiqueta real Churn observada después.
  La relación entre variables y abandono también cambia (concept drift simulado).
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
rng = np.random.default_rng(7)

ref = pd.read_csv(ROOT / "data" / "telco_original.csv")
ref["TotalCharges"] = (ref["tenure"] * ref["MonthlyCharges"]).round(2)
ref = ref[["tenure", "MonthlyCharges", "TotalCharges", "Contract", "InternetService", "Churn"]]

n = 300
tenure = np.clip(rng.gamma(2.0, 9.0, n).round().astype(int), 1, 72)            # Clientes más nuevos
monthly = np.clip(rng.normal(88, 16, n), 30, 130).round(2)                       # Cargos más altos
contract = rng.choice(["Month-to-month", "One year", "Two year"], n, p=[0.72, 0.18, 0.10])
internet = rng.choice(["DSL", "Fiber optic", "No"], n, p=[0.33, 0.34, 0.33])    # Sin cambio
cur = pd.DataFrame({
    "tenure": tenure, "MonthlyCharges": monthly,
    "TotalCharges": (tenure * monthly).round(2),
    "Contract": contract, "InternetService": internet,
})

# Concept drift: tras una promoción, los contratos anuales también abandonan y el cargo pesa menos
p = np.select([cur.Contract == "Month-to-month", cur.Contract == "One year"], [0.42, 0.40], 0.12)
p = p + np.where(cur.InternetService == "DSL", 0.08, 0.0) + np.where(cur.tenure < 12, 0.15, 0.0)
churn = np.where(rng.random(n) < p, "Yes", "No")

ref.to_csv(ROOT / "data" / "reference.csv", index=False)
cur.to_csv(ROOT / "data" / "current.csv", index=False)
cur.assign(Churn=churn).to_csv(ROOT / "data" / "current_with_labels.csv", index=False)
print("reference:", ref.shape, "| current:", cur.shape)
