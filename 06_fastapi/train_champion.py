"""Genera models/champion.joblib (ya incluido en el proyecto; no es necesario ejecutarlo).

Champion de la práctica 4: Regresión Logística (mayor ROC-AUC).
Se entrena con las cinco variables que recibe la API. TotalCharges no viene en el
dataset de práctica, así que se calcula como tenure * MonthlyCharges.
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parent
NUMERIC = ["tenure", "MonthlyCharges", "TotalCharges"]
CATEGORICAL = ["Contract", "InternetService"]

df = pd.read_csv(ROOT / "data" / "telco.csv")
df["TotalCharges"] = df["tenure"] * df["MonthlyCharges"]
X = df[NUMERIC + CATEGORICAL]
y = (df["Churn"] == "Yes").astype(int)                      # 1 = abandono

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)
model = Pipeline([
    ("preprocessing", ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC),
        ("categorical", OneHotEncoder(
            categories=[["Month-to-month", "One year", "Two year"], ["DSL", "Fiber optic", "No"]],
            handle_unknown="ignore"), CATEGORICAL),
    ])),
    ("classifier", LogisticRegression(C=1.0, max_iter=1000, random_state=42)),
])
model.fit(X_train, y_train)
pred = model.predict(X_test); prob = model.predict_proba(X_test)[:, 1]
print(f"Accuracy {accuracy_score(y_test, pred):.3f} | F1 {f1_score(y_test, pred):.3f} | ROC-AUC {roc_auc_score(y_test, prob):.3f}")

(ROOT / "models").mkdir(exist_ok=True)
joblib.dump(model, ROOT / "models" / "champion.joblib")
print("Guardado en models/champion.joblib")
