# Telco Customer Churn — práctica de Git

**Nota sobre datos:** `data/telco_demo.csv` es un dataset **sintético**, con columnas inspiradas en Telco Customer Churn. No es una copia de Kaggle ni contiene datos de clientes reales. Se incluye para que la práctica funcione sin descargar nada. Para las prácticas posteriores se puede sustituir por el dataset real de Kaggle, revisando nombres y esquema.

## Requisitos
- Windows con Python 3.10+ y Git instalados.
- Visual Studio Code con terminal integrada (PowerShell).

## Ejecutar
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m src.train --model forest
.\.venv\Scripts\python.exe -m src.train --model logistic
.\.venv\Scripts\python.exe -m src.train --model svm
```

Si `py` no existe, sustituirlo por `python`. La ejecución mediante `.venv\Scripts\python.exe` evita cambiar la política de ejecución de PowerShell.

## Git
Seguir `GUIA_GIT.md`. Este ZIP no contiene `.git`, para que cada alumno inicialice su propio repositorio.

Este proyecto utiliza Regresión Logística, Random Forest y SVM.

Evaluación de modelos
Utilizaremos Accuracy, F1 y ROC-AUC
Modelo SVM

Modelo principal: SVM

Explicación: La accuracy es el porcentaje de predicciones correctas sobre el total; la precision indica, de los casos que el modelo predijo como positivos, cuántos lo eran realmente; el recall mide, de todos los positivos reales, cuántos logró detectar el modelo; y el F1-score es la media armónica de precision y recall, que resume en una sola cifra el equilibrio entre ambas.

Resultados del proyecto