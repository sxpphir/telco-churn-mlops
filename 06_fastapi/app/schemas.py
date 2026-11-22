from typing import Literal                          # Restringir categorías

from pydantic import BaseModel, Field               # Definir esquema validado


class CustomerInput(BaseModel):                     # Datos de un cliente
    tenure: int = Field(ge=0, le=100)               # Meses entre 0 y 100
    MonthlyCharges: float = Field(ge=0)             # Cargo mensual no negativo
    TotalCharges: float = Field(ge=0)               # Cargo total no negativo
    Contract: Literal[                              # Contratos permitidos
        "Month-to-month", "One year", "Two year"
    ]
    InternetService: Literal[                       # Servicios permitidos
        "DSL", "Fiber optic", "No"
    ]
