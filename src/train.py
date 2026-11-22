import json
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "telco_demo.csv"
MODEL_PATH = ROOT / "models" / "model.joblib"


def build_model(name):
    numeric = ["tenure", "MonthlyCharges"]
    categorical = ["Contract", "InternetService"]
    preprocessing = ColumnTransformer([
        ("numeric", StandardScaler(), numeric),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical),
    ])
    classifiers = {
        "logistic": LogisticRegression(max_iter=1000, random_state=42),
        "forest": RandomForestClassifier(n_estimators=80, max_depth=5, random_state=42),
        "svm": SVC(kernel="rbf", C=1.0, probability=True, random_state=42),
    }
    if name not in classifiers:
        raise ValueError(f"Modelo desconocido: {name}")
    return Pipeline([("preprocessing", preprocessing), ("classifier", classifiers[name])])


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["logistic", "forest", "svm"], default="forest")
    args = parser.parse_args()
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns="Churn")
    y = (df["Churn"] == "Yes").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )
    model = build_model(args.model)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]
    MODEL_PATH.parent.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo: {args.model}")
    print(f"Accuracy: {accuracy_score(y_test, pred):.3f}")
    print(f"F1: {f1_score(y_test, pred, zero_division=0):.3f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, proba):.3f}")
    print(f"Guardado en: {MODEL_PATH}")
    metrics = {                                   # Métricas para DVC (dvc metrics show)
        "modelo": args.model,
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
    }
    (ROOT / "metrics.json").write_text(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
