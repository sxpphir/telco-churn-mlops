"""Cálculo de métricas de evaluación para un modelo ya entrenado."""
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


def evaluate(model, X_test, y_test):
    """Devuelve Accuracy, F1 y ROC-AUC sobre el conjunto de prueba."""
    y_pred = model.predict(X_test)                 # Clases predichas
    y_prob = model.predict_proba(X_test)[:, 1]     # Probabilidad de churn
    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_test, y_prob),
    }
