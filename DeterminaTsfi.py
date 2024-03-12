# calcular la fracción de semestre (t_fsi) entre dos fechas
from datetime import datetime
import DB

def calcular_fraccion_semestre(fecha_deposito_str,fecha_corte_str):

    fecha_deposito = datetime.strptime(fecha_deposito_str, '%Y-%m-%d')
    fecha_corte = datetime.strptime(fecha_corte_str, '%Y-%m-%d')
    

    # Calcular la fracción del semestre
    t_fsi = (fecha_corte - fecha_deposito).days

    return t_fsi   

