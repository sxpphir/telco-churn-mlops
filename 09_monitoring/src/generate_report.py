from pathlib import Path                         # Manejar archivos y carpetas

import pandas as pd                              # Leer y manipular datos
from evidently import Report                     # Generar reportes
from evidently.presets import DataDriftPreset    # Configurar análisis de drift

FEATURES = ["tenure", "MonthlyCharges", "TotalCharges", "Contract", "InternetService"]

reference = pd.read_csv("data/reference.csv")[FEATURES]   # Cargar datos históricos
current = pd.read_csv("data/current.csv")[FEATURES]       # Cargar datos nuevos

report = Report(                                 # Crear reporte
    [DataDriftPreset()]                          # Incluir análisis de data drift
)

result = report.run(                             # Ejecutar comparación
    reference_data=reference,                    # Dataset de referencia
    current_data=current,                        # Dataset actual
)

Path("reports").mkdir(exist_ok=True)             # Crear carpeta de reportes
result.save_html("reports/data_drift.html")      # Guardar reporte HTML
print("Reporte guardado en reports/data_drift.html")

# Resumen en consola de las métricas calculadas por Evidently
for metric in result.dict()["metrics"]:
    print(f"{metric['metric_id']}: {metric['value']}")
