import enum
from datetime import datetime

class EnumMeses(enum.Enum):
    Enero = 1
    Febrero = 2
    Marzo = 3
    Abril = 4
    Mayo = 5
    Junio = 6
    Julio = 7
    Agosto = 8
    Septiembre = 9
    Octubre = 10
    Noviembre = 11
    Diciembre = 12

def obtener_nombre_mes(fecha):
    mes_numero = fecha.month
    mes_nombre = EnumMeses(mes_numero).name
    return mes_nombre