# Proyecto - Introducción a MLOps: Desarrollo, Versionado y Automatización de Modelos de Machine Learning

**Alumna:** Ana Michel Garcia Perez · **Materia:** Minería de Datos · **Profesor:** Gustavo Daniel Vega Magdaleno

Caso de estudio: **predicción de abandono de clientes (Telco Customer Churn)**. A partir de la antigüedad,
el cargo mensual, el cargo total, el tipo de contrato y el servicio de internet de un cliente, el modelo
predice si abandonará el servicio y con qué probabilidad.

- Modelo Champion: **Regresión Logística** (ROC-AUC 0.70, Accuracy 0.77), comparada contra Random Forest y SVM.
- Reporte: [`docs/Reporte_Final_MLOps.pdf`](docs/Reporte_Final_MLOps.pdf) · Anexo con todas las evidencias: [`docs/Anexo_Evidencias_MLOps.pdf`](docs/Anexo_Evidencias_MLOps.pdf)
- Guía para la demostración: [`DEMO.md`](DEMO.md)

## Estructura

| Carpeta | Herramienta | Qué contiene |
|---|---|---|
| raíz (`src/`, `data/`, `dvc.yaml`) | Git, GitHub, DVC | Código de entrenamiento, dataset versionado con DVC (`.dvc`), pipeline `dvc.yaml` + `dvc.lock` y `metrics.json` |
| `04_mlflow/` | MLflow | Preprocesamiento, entrenamiento de 3 modelos registrados en MLflow, Model Registry y alias `champion` |
| `05_airflow/` | Apache Airflow | DAG `telco_training_pipeline` (validar → entrenar → seleccionar champion → reporte) con Docker Compose |
| `06_fastapi/` | FastAPI | API `/predict`, `/health` y formulario HTML con el modelo Champion |
| `07_docker/` | Docker | Dockerfile para empaquetar la API |
| `08_cicd/` | GitHub Actions | Pruebas con pytest y workflow CI/CD que publica la imagen en GHCR |
| `09_monitoring/` | Evidently AI | Detección de data drift, monitoreo de predicciones y de rendimiento con alerta |
| `docs/` | — | Reporte PDF y anexo de evidencias |

El historial de commits, ramas y Pull Requests de este repositorio corresponde a las prácticas de Git y GitHub.

Repositorio adicional:
- CI/CD con GitHub Actions (workflow en ejecución e imagen publicada): https://github.com/sxpphir/telco-churn-cicd
- Imagen Docker publicada: `ghcr.io/sxpphir/telco-churn-cicd:latest`

## Requisitos
- Python 3.11 o superior, Git y Docker Desktop (motor Linux).
- Cada carpeta tiene su propio `requirements.txt` y `README.md` con instrucciones.

## Ejecución rápida

**Aplicación web (la forma más rápida, con Docker):**
```bat
cd 07_docker
docker build -t telco-api:v1 .
docker run -d --name telco-api -p 8000:8000 telco-api:v1
```
Abrir http://localhost:8000 (formulario) y http://localhost:8000/docs (API).

**DVC (pipeline):**
```bat
python -m pip install -r requirements.txt dvc
dvc repro
dvc dag
dvc metrics show
```
> El remoto de DVC del proyecto original es una carpeta local (`../../dvc_storage`). En este repositorio el
> dataset se incluye también en `04_mlflow/data/telco.csv`; para reproducir el pipeline basta copiarlo a
> `data/telco_demo.csv`.

**MLflow:**
```bat
cd 04_mlflow
python -m pip install -r requirements.txt
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 127.0.0.1 --port 5000
REM En otra terminal:
python -m src.train
python -m src.registry register --run-id <RUN_ID>
python -m src.registry champion --version 1
python -m src.registry load
```

**Airflow + MLflow:**
```bat
cd 05_airflow
docker compose up -d --build
```
Airflow: http://localhost:8080 (admin / admin) · MLflow: http://localhost:5000

**Pruebas (CI):**
```bat
cd 08_cicd
python -m pip install -r requirements.txt
python -m pytest -v
```

**Monitoreo:**
```bat
cd 09_monitoring
python -m pip install -r requirements.txt
python src/generate_report.py
python src/prediction_monitor.py
python src/performance_monitor.py
```
Abrir `reports/data_drift.html`. Los datos del periodo actual (`current.csv`) son simulados con cambios
intencionales, generados por `src/make_datasets.py`.
