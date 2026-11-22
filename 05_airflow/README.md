# Práctica 5 — Apache Airflow (Telco Customer Churn)

Requiere Docker Desktop abierto (motor Linux). Comandos en PowerShell dentro de `05_airflow_telco`.

## Iniciar
```powershell
docker --version
docker compose version
docker info
docker compose up -d --build
docker compose ps
```
La primera vez tarda varios minutos.

- Airflow: http://localhost:8080  — usuario **admin**, contraseña **admin**
- MLflow:  http://localhost:5000

> Si tienes abierto el MLflow de la práctica 4 en el puerto 5000, detenlo antes (Ctrl+C en su terminal).

## Tareas del DAG `telco_training_pipeline`
1. `validar_datos` → `src/validate.py`
2. `entrenar_modelos` → `src/train.py` (registra los 3 modelos en MLflow)
3. `seleccionar_champion` → `src/select_champion.py` (mayor ROC-AUC → alias champion)
4. (Actividad 5) `generar_reporte` → `src/report.py`, función `generate_report`

## Ver logs o detener
```powershell
docker compose logs airflow --tail 50
docker compose down
```
