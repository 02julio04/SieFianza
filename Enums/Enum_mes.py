import enum
from datetime import datetime

class EnumMeses(enum.Enum):
    Enero = "January"
    Febrero = "February"
    Marzo = "March"
    Abril = "April"
    Mayo = "May"
    Junio = "June"
    Julio = "July"
    Agosto = "August"
    Septiembre = "September"
    Octubre = "October"
    Noviembre = "November"
    Diciembre = "December"

def obtener_nombre_mes(fecha):
    mes = datetime.strptime(fecha, "%Y-%m-%d").strftime("%B")
    mes_nombre = EnumMeses(mes).name
    return mes_nombre