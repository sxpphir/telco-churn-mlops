"""Entrena los tres clasificadores y registra cada uno como un run en MLflow.

Uso (con el servidor de MLflow encendido en otra terminal):
    python -m src.train                  # Entrena los tres modelos
    python -m src.train --model svm      # Entrena solo uno
"""
import argparse
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

from src.evaluate import evaluate
from src.preprocess import build_preprocessor, load_data, split_data

ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"

TRACKING_URI = "http://127.0.0.1:5000"   # Servidor local de MLflow
EXPERIMENT = "Telco_Churn"               # Nombre del experimento

# Configuración real de cada modelo. Estos mismos valores se registran en
# MLflow, así que lo registrado siempre coincide con lo entrenado.
CONFIGS = {
    "logistic": {
        "run_name": "Logistic_Regression",
        "params": {"C": 1.0, "max_iter": 1000},
        "build": lambda p: LogisticRegression(C=p["C"], max_iter=p["max_iter"], random_state=42),
    },
    "forest": {
        "run_name": "Random_Forest",
        "params": {"n_estimators": 80, "max_depth": 5},
        "build": lambda p: RandomForestClassifier(
            n_estimators=p["n_estimators"], max_depth=p["max_depth"], random_state=42
        ),
    },
    "svm": {
        "run_name": "SVM_RBF",
        "params": {"C": 1.0, "gamma": "scale", "kernel": "rbf"},
        # probability=True es necesario para usar predict_proba() y calcular ROC-AUC
        "build": lambda p: SVC(
            C=p["C"], gamma=p["gamma"], kernel=p["kernel"], probability=True, random_state=42
        ),
    },
}


def train_one(name, X_train, X_test, y_train, y_test):
    cfg = CONFIGS[name]
    model = Pipeline([
        ("preprocessing", build_preprocessor()),     # Se ajusta solo con X_train
        ("classifier", cfg["build"](cfg["params"])),
    ])

    with mlflow.start_run(run_name=cfg["run_name"]) as run:
        model.fit(X_train, y_train)
        metrics = evaluate(model, X_test, y_test)

        mlflow.log_param("modelo", cfg["run_name"])
        mlflow.log_params(cfg["params"])
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            sk_model=model,                # Incluye el preprocesamiento
            name="model",                  # Artefacto: runs:/<run_id>/model
            input_example=X_train.head(3),
            serialization_format="cloudpickle",   # Evita el bloqueo de skops con RandomForest
        )

        MODELS_DIR.mkdir(exist_ok=True)
        joblib.dump(model, MODELS_DIR / f"{name}.joblib")

        print(f"\n[{cfg['run_name']}]  run_id = {run.info.run_id}")
        for k, v in metrics.items():
            print(f"  {k:9s}: {v:.3f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["all", *CONFIGS], default="all")
    args = parser.parse_args()

    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    X, y = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)   # Misma partición para todos

    names = list(CONFIGS) if args.model == "all" else [args.model]
    for name in names:
        train_one(name, X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    main()
