FROM python:3.11-slim
# Utilizar una imagen ligera de Python 3.11

WORKDIR /app
# Establecer el directorio de trabajo

COPY requirements.txt .
# Copiar la lista de dependencias

RUN pip install --no-cache-dir -r requirements.txt
# Instalar las librerias dentro de la imagen

COPY app/ ./app/
# Copiar los archivos de FastAPI

COPY models/ ./models/
# Copiar el modelo entrenado

COPY templates/ ./templates/
# Copiar la interfaz HTML

EXPOSE 8000
# Documentar el puerto utilizado por FastAPI

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# Iniciar el servidor cuando se ejecute el contenedor
