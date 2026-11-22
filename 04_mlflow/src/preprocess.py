"""Carga de datos, partición y preprocesamiento del dataset Telco Churn.

El preprocesador se devuelve SIN ajustar: se ajusta solo con los datos de
entrenamiento dentro del Pipeline (model.fit(X_train, ...)) y después se
aplica a los datos de prueba, evitando fuga de información.
"""
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "telco.csv"

NUMERIC = ["tenure", "MonthlyCharges"]          # Variables numéricas
CATEGORICAL = ["Contract", "InternetService"]   # Variables categóricas
TARGET = "Churn"                                # Variable objetivo

TEST_SIZE = 0.25        # Proporción de prueba
RANDOM_STATE = 42       # Semilla para que los tres modelos usen la misma partición


def load_data(path=DATA_PATH):
    """Lee el CSV y separa X (entradas) e y (1 = el cliente se va)."""
    df = pd.read_csv(path)
    X = df[NUMERIC + CATEGORICAL]
    y = (df[TARGET] == "Yes").astype(int)
    return X, y


def split_data(X, y):
    """Partición estratificada; es la misma para todos los modelos."""
    return train_test_split(
        X, y, test_size=TEST_SIZE, stratify=y, random_state=RANDOM_STATE
    )


def build_preprocessor():
    """Escala numéricas y codifica categóricas (sin ajustar todavía)."""
    return ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
