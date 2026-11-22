# Guía para la demostración en clase

Tiempo estimado: 10 minutos. Antes de clase: abre **Docker Desktop** y espera a que diga *Engine running*.

## 0. Preparar (antes de que te toque, ~3 min)
Abre dos terminales en la carpeta del proyecto.

**Terminal 1 — aplicación web:**
```bat
cd 07_docker
docker build -t telco-api:v1 .
docker run -d --name telco-api -p 8000:8000 telco-api:v1
```
**Terminal 2 — Airflow + MLflow:**
```bat
cd 05_airflow
docker compose up -d
```
Ten abiertas estas pestañas en el navegador:
- http://localhost:8000 (formulario) y http://localhost:8000/docs
- http://localhost:8080 (Airflow, admin / admin)
- http://localhost:5000 (MLflow)
- https://github.com/sxpphir/telco-churn-cicd/actions
- `09_monitoring/reports/data_drift.html`

## 1. La aplicación funcionando (lo principal)
1. En **localhost:8000** haz una predicción con el cliente de ejemplo (5 meses, 85.5, Month-to-month,
   Fiber optic) → *Abandona (1), 71.4 %, riesgo Alto*.
2. Cambia a 60 meses, cargo 40, Two year, DSL → *Permanece (0), 2.1 %, riesgo Bajo*.
3. En **/docs** muestra `POST /predict` y prueba `tenure = -10` → error **422** (validación con Pydantic).
4. Muestra **/health** → `{"status": "ok"}`.
5. En la terminal: `docker ps` → la app corre dentro de un contenedor.

## 2. Componentes MLOps (1 minuto cada uno)
| Herramienta | Qué mostrar | Qué decir |
|---|---|---|
| Git / GitHub | `git log --oneline --graph --all` en `01_git_telco` y el repo en GitHub | Ramas `feature/*`, merges, conflicto resuelto y Pull Request |
| DVC | `dvc dag` y `dvc metrics show` | Git guarda el puntero `.dvc` y DVC el dataset; `dvc repro` reproduce el entrenamiento |
| MLflow | Experimento *Telco_Churn*, Compare y Models → `TelcoChurnClassifier@champion` | Cada run guarda parámetros, métricas y modelo; el champion es el de mayor ROC-AUC |
| Airflow | DAG `telco_training_pipeline` → **Trigger** y vista Graph | Automatiza validar → entrenar → seleccionar champion → reporte |
| Docker | `docker images` (v1, v2) y `docker ps` | La app trae su propio Python y librerías: funciona igual en cualquier equipo |
| GitHub Actions | Pestaña Actions: runs #1 ✅, #2 ❌, #3 ✅ | Cada push corre pytest; si falla, no se publica la imagen en GHCR |
| Monitoreo | `data_drift.html` y `python src/performance_monitor.py` | Drift en 4 de 5 variables; ROC-AUC 0.80 → 0.52 → ALERTA |

## 3. Preguntas probables
- **¿Qué predice el modelo?** Si un cliente abandonará el servicio (Churn) y con qué probabilidad.
- **¿Por qué Regresión Logística?** Tuvo el mayor ROC-AUC (0.70). SVM tuvo mejor F1 (0.50); con ROC-AUC
  elegimos el modelo que mejor ordena a los clientes por riesgo.
- **¿Los resultados son buenos?** Moderados: superan el azar, pero el F1 ≈ 0.49 indica que se escapan
  abandonos. Se debe a pocos datos (360) y pocas variables; mejoraría ajustando el umbral o con más variables.
- **¿Por qué el preprocesamiento va en un Pipeline?** Para ajustarlo solo con los datos de entrenamiento
  (evitar fuga de información) y que el modelo guardado incluya la transformación.
- **Diferencia entre Git y DVC:** Git versiona código; DVC versiona datos grandes guardando solo un hash en Git.
- **Diferencia entre imagen y contenedor:** la imagen es la plantilla; el contenedor es su ejecución.
- **¿Qué pasa si una prueba falla en CI?** El job `test` falla y el job `docker` no se ejecuta (`needs: test`),
  así no se publica una versión defectuosa.
- **¿Data drift significa reentrenar?** No automáticamente. Primero se investiga; aquí sí se justifica evaluar
  un reentrenamiento porque además cayó el rendimiento (ROC-AUC 0.80 → 0.52).
- **¿Por qué los contenedores se comunican con `http://mlflow:5000` y no `localhost`?** Dentro de Docker
  Compose cada servicio se resuelve por su nombre.

## Al terminar
```bat
docker stop telco-api && docker rm telco-api
cd 05_airflow && docker compose down
```
