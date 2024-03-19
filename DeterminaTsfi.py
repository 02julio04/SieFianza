# calcular la fracción de semestre (t_fsi) entre dos fechas
from datetime import datetime

def calcular_fraccion_semestre(fecha_deposito_str,fecha_corte_str):

    # Convertir solo si las fechas de entrada son cadenas
    if isinstance(fecha_deposito_str, str):
        fecha_deposito = datetime.strptime(fecha_deposito_str, '%Y-%m-%d')
    else:
        fecha_deposito = fecha_deposito_str  # Si ya es datetime, lo usa directamente

    if isinstance(fecha_corte_str, str):
        fecha_corte = datetime.strptime(fecha_corte_str, '%Y-%m-%d')
    else:
        fecha_corte = fecha_corte_str
    
    # Obteniendo el año y mes de la fecha de depósito
    year = fecha_deposito.year
    month = fecha_deposito.month
    
    # Definiendo la fecha del próximo semestre
    if month <= 6:  # Si la fecha de depósito es antes de junio, el próximo semestre es junio de este año
        prox_semestre = datetime(year, 6, 30)
    else:  # Si la fecha de depósito es en julio o después, el próximo semestre es diciembre de este año
        prox_semestre = datetime(year, 12, 31)
    
    # Calcular la fracción del semestre
    #print(f"t_fsi = ({prox_semestre} - {fecha_deposito}).days = {(prox_semestre - fecha_deposito).days}")
    
    t_fsi = (prox_semestre - fecha_deposito).days / 365
    #print(f"t_fsi = {t_fsi}")
    
    return t_fsi

