# calcular la fracción de semestre (t_fsi) entre dos fechas
from datetime import datetime
from DB import Buscar_en_BD

def calcular_fraccion_semestre(fecha_deposito_str,fecha_corte_str):
    # Solicitar al usuario las fechas de depósito y corte
    #fecha_deposito_str = input("Digite la fecha del depósito (formato YYYYMMDD): ")
    #fecha_corte_str = input("Digite la fecha de corte (formato YYYYMMDD): ")
    
    #fecha_deposito_str,fecha_corte_str = Buscar_en_BD()
    #print (fecha_corte_str,fecha_deposito_str)
    fecha_deposito = datetime.strptime(fecha_deposito_str, '%Y-%m-%d')
    fecha_corte = datetime.strptime(fecha_corte_str, '%Y-%m-%d')
    

    # Calcular la fracción del semestre
    t_fsi = (fecha_corte - fecha_deposito).days
    
    print(f"La fracción del semestre (t_fsi) es: {t_fsi} días")

    return t_fsi,fecha_deposito,fecha_corte    

# calcular_fraccion_semestre()
