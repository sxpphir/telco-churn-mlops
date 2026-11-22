"""Model Registry: registrar el ganador, asignar el alias champion y recuperarlo.

Uso:
    python -m src.registry register --run-id <RUN_ID>   # Actividad 6
    python -m src.registry champion --version 1         # Actividad 7
    python -m src.registry load                         # Actividad 8
"""
import argparse

import mlflow
import mlflow.pyfunc
from mlflow import MlflowClient

from src.preprocess import load_data

TRACKING_URI = "http://127.0.0.1:5000"
MODEL_NAME = "TelcoChurnClassifier"


def register(run_id):
    model_uri = f"runs:/{run_id}/model"
    mv = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
    print(f"Registrado {MODEL_NAME} versión {mv.version} desde {model_uri}")


def set_champion(version):
    client = MlflowClient(tracking_uri=TRACKING_URI)
    client.set_registered_model_alias(name=MODEL_NAME, alias="champion", version=str(version))
    print(f"Alias 'champion' asignado a {MODEL_NAME} versión {version}")


def load_champion():
    modelo = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}@champion")
    print(f"Modelo cargado: models:/{MODEL_NAME}@champion")
    X, _ = load_data()
    muestra = X.head(5)                       # Mismas columnas que en el entrenamiento
    print(muestra.assign(prediccion=modelo.predict(muestra)).to_string(index=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("register")
    r.add_argument("--run-id", required=True)
    c = sub.add_parser("champion")
    c.add_argument("--version", required=True)
    sub.add_parser("load")
    args = parser.parse_args()

    mlflow.set_tracking_uri(TRACKING_URI)
    if args.cmd == "register":
        register(args.run_id)
    elif args.cmd == "champion":
        set_champion(args.version)
    else:
        load_champion()


if __name__ == "__main__":
    main()
