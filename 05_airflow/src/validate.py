"""Tarea 1 del DAG: validar que el dataset existe y tiene las columnas esperadas."""
from pathlib import Path

import pandas as pd

DATA_PATH = "/opt/airflow/data/telco.csv"              # Restaurar ruta correcta

REQUIRED_COLUMNS = ["tenure", "MonthlyCharges", "Contract", "InternetService", "Churn"]


def validate_data():
    path = Path(DATA_PATH)
    if not path.exists():
        raise FileNotFoundError(f"No se encontró el dataset en {path}")

    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("El dataset está vacío")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en el dataset: {missing}")

    print(f"Dataset válido: {path} | {len(df)} filas | columnas: {list(df.columns)}")
    return {"filas": len(df)}