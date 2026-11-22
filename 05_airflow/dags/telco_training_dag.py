from datetime import datetime                         # Manejar fechas

from airflow import DAG                               # Definir DAG
from airflow.operators.python import PythonOperator   # Ejecutar funciones

from src.validate import validate_data                # Validar dataset
from src.train import train_models                    # Entrenar y registrar modelos
from src.select_champion import select_champion      # Seleccionar Champion
from src.report import generate_report

with DAG(                                             # Definir flujo
    dag_id="telco_training_pipeline",                 # Identificador
    start_date=datetime(2026, 1, 1),                  # Fecha inicial
    schedule=None,                                    # Ejecución manual
    catchup=False,                                    # Evitar ejecuciones pasadas
) as dag:

    validar = PythonOperator(                         # Primera tarea
        task_id="validar_datos",
        python_callable=validate_data,
    )

    entrenar = PythonOperator(                        # Segunda tarea
        task_id="entrenar_modelos",
        python_callable=train_models,
    )

    seleccionar = PythonOperator(                     # Tercera tarea
        task_id="seleccionar_champion",
        python_callable=select_champion,
    )

    reporte = PythonOperator(                         # Cuarta tarea
        task_id="generar_reporte",
        python_callable=generate_report,
    )

    validar >> entrenar >> seleccionar >> reporte     # Nuevo orden
    
