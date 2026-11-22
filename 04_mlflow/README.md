# Práctica 4 — MLflow (Telco Customer Churn)

Todos los comandos se ejecutan en PowerShell, dentro de la carpeta `04_mlflow_telco`.

## 1. Instalar
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
mlflow --version
```

## 2. Iniciar MLflow (terminal 1, déjala abierta)
```powershell
.\.venv\Scripts\Activate.ps1
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlartifacts --host 127.0.0.1 --port 5000
```
Abre http://127.0.0.1:5000 en el navegador.

## 3. Entrenar y registrar los tres modelos (terminal 2)
```powershell
.\.venv\Scripts\Activate.ps1
python -m src.train
```
Se crean tres runs en el experimento `Telco_Churn`: Logistic_Regression, Random_Forest y SVM_RBF.
La terminal imprime el `run_id` y las métricas de cada uno.

## 4. Comparar
En MLflow: experimento Telco_Churn → seleccionar los 3 runs → **Compare**.
El modelo con mayor **ROC-AUC** es el candidato a Champion.

## 5. Registrar el ganador
```powershell
python -m src.registry register --run-id PEGA_AQUI_EL_RUN_ID
```

## 6. Asignar el alias champion
```powershell
python -m src.registry champion --version 1
```
(o desde la interfaz: Models → TelcoChurnClassifier → versión → Add alias)

## 7. Recuperar el Champion
```powershell
python -m src.registry load
```
