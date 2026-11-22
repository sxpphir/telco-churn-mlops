"""Tarea opcional (Actividad 5): generar un reporte final de la ejecución."""
from datetime import datetime
from pathlib import Path

REPORT_PATH = Path("/opt/airflow/data/reporte_final.txt")


def generate_report(**context):
    ti = context["ti"]
    results = ti.xcom_pull(task_ids="entrenar_modelos") or {}
    champion = ti.xcom_pull(task_ids="seleccionar_champion") or {}

    lines = [
        "REPORTE FINAL - Telco Churn",
        f"Fecha: {datetime.now():%Y-%m-%d %H:%M:%S}",
        "",
        f"{'Modelo':22s}{'Accuracy':>10s}{'F1':>8s}{'ROC-AUC':>10s}",
    ]
    for name, r in results.items():
        lines.append(f"{name:22s}{r['accuracy']:>10.3f}{r['f1']:>8.3f}{r['roc_auc']:>10.3f}")
    lines += ["", f"Champion: {champion.get('modelo')} (versión {champion.get('version')})"]

    text = "\n".join(lines)
    print(text)
    REPORT_PATH.write_text(text, encoding="utf-8")
    print(f"Reporte guardado en {REPORT_PATH}")
