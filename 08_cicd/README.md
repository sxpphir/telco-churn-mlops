# Telco Churn CI/CD

Aplicación FastAPI con el modelo Champion (Regresión Logística) para predecir abandono de clientes.
Incluye pruebas con pytest, Dockerfile y un workflow de GitHub Actions que prueba, construye y
publica la imagen en GitHub Container Registry (GHCR).

## Pruebas locales (CMD)
```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m pytest -v
```
