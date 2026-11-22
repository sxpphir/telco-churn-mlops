"""Tarea 3 del DAG: elegir el modelo con mayor ROC-AUC y asignarle el alias champion."""
import os

import mlflow
from mlflow import MlflowClient

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
MODEL_NAME = "TelcoChurnClassifier"


def select_champion(**context):
    results = context["ti"].xcom_pull(task_ids="entrenar_modelos")   # Resultados de la tarea anterior
    if not results:
        raise ValueError("No se recibieron resultados de entrenar_modelos")

    best_name = max(results, key=lambda n: results[n]["roc_auc"])
    best = results[best_name]
    print(f"Modelo ganador por ROC-AUC: {best_name} ({best['roc_auc']})")

    mlflow.set_tracking_uri(TRACKING_URI)
    mv = mlflow.register_model(model_uri=f"runs:/{best['run_id']}/model", name=MODEL_NAME)

    client = MlflowClient(tracking_uri=TRACKING_URI)
    client.set_registered_model_alias(name=MODEL_NAME, alias="champion", version=mv.version)
    print(f"Alias 'champion' asignado a {MODEL_NAME} versión {mv.version}")

    return {"modelo": best_name, "version": str(mv.version), **best}
