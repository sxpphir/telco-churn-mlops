# Práctica 7 — Docker (Telco Customer Churn)

Aplicación FastAPI de la práctica 6 (con risk_level) + modelo Champion (Regresión Logística).

```bat
docker build -t telco-api:v1 .
docker images
docker run -d --name telco-api -p 8000:8000 telco-api:v1
docker ps
```
- http://localhost:8000/docs
- http://localhost:8000/health
