"""Tarea 2 del DAG: entrenar los tres clasificadores y registrarlos en MLflow."""
import os

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC

DATA_PATH = "/opt/airflow/data/telco.csv"
# Dentro de Docker se usa el nombre del servicio (mlflow), no localhost
TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
EXPERIMENT = "Telco_Churn"

NUMERIC = ["tenure", "MonthlyCharges"]
CATEGORICAL = ["Contract", "InternetService"]

CONFIGS = {
    "Logistic_Regression": {
        "params": {"C": 1.0, "max_iter": 1000},
        "build": lambda p: LogisticRegression(C=p["C"], max_iter=p["max_iter"], random_state=42),
    },
    "Random_Forest": {
        "params": {"n_estimators": 80, "max_depth": 5},
        "build": lambda p: RandomForestClassifier(
            n_estimators=p["n_estimators"], max_depth=p["max_depth"], random_state=42
        ),
    },
    "SVM_RBF": {
        "params": {"C": 1.0, "gamma": "scale", "kernel": "rbf"},
        "build": lambda p: SVC(
            C=p["C"], gamma=p["gamma"], kernel=p["kernel"], probability=True, random_state=42
        ),
    },
}


def _preprocessor():
    return ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])


def train_models():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT)

    df = pd.read_csv(DATA_PATH)
    X = df[NUMERIC + CATEGORICAL]
    y = (df["Churn"] == "Yes").astype(int)
    X_train, X_test, y_train, y_test = train_test_split(       # Misma partición para los tres
        X, y, test_size=0.25, stratify=y, random_state=42
    )

    results = {}
    for name, cfg in CONFIGS.items():
        model = Pipeline([
            ("preprocessing", _preprocessor()),                   # Se ajusta solo con X_train
            ("classifier", cfg["build"](cfg["params"])),
        ])
        with mlflow.start_run(run_name=name) as run:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)[:, 1]
            metrics = {
                "accuracy": accuracy_score(y_test, y_pred),
                "f1": f1_score(y_test, y_pred, zero_division=0),
                "roc_auc": roc_auc_score(y_test, y_prob),
            }
            mlflow.log_param("modelo", name)
            mlflow.log_params(cfg["params"])
            mlflow.log_metrics(metrics)
            mlflow.set_tag("origen", "airflow")
            mlflow.sklearn.log_model(model, artifact_path="model")

        results[name] = {"run_id": run.info.run_id, **{k: round(v, 4) for k, v in metrics.items()}}
        print(f"{name}: {results[name]}")

    return results                                              # Se envía por XCom a la siguiente tarea
