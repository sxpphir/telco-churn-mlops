FROM apache/airflow:2.10.5-python3.11

COPY requirements.txt /requirements.txt
# Se fija la versión de Airflow para que pip no la cambie al instalar las dependencias
RUN pip install --no-cache-dir "apache-airflow==2.10.5" -r /requirements.txt
