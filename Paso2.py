'''
AGREGAR al depósito capitalizado por la fracción de semestre inicial Dfsi, la
capitalización de los intereses generados para los semestres estándares completos
sucesivos que apliquen
'''

import DB
from datetime import datetime, timedelta
server = 'PEDROJULIO'
database = 'Db_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
db = DB.Database(conn_str)

def calcular_capitalizacion_por_semestre_interactivo(D_calc,i_fsi_db,semestres,fecha_inicio,fecha_corte_str): #fecha_deposito,#fecha_corte
    # Solicitar al usuario que ingrese los datos necesarios
    D = D_calc # float(input("Por favor, ingresa el monto del depósito inicial (D): "))
    i_fsi = i_fsi_db # float(input("Por favor, ingresa la tasa de interés anual como porcentaje (i_fsi): "))
    n = semestres # int(input("Por favor, ingresa el número total de semestres a calcular: "))

    # Convertir la tasa de interés anual a una tasa semestral
    i_fsi = i_fsi / 100
    i_semestral = i_fsi * 0.5  # Tasa de interés para medio año

    D_actual = D
    depositos_por_semestre = [D]
    ult_deposito = 0
    ult_tasa = 0

    # Convertir la fecha de inicio a un objeto datetime para manipulación
    fecha_inicio_dt = fecha_inicio if isinstance(fecha_inicio, datetime) else datetime.strptime(fecha_inicio, "%Y-%m-%d")
   # Determinar el año y el semestre base
    año_base = fecha_inicio_dt.year
    mes_base = fecha_inicio_dt.month

    if mes_base > 6:  # Si el mes base es después de junio, empezar en diciembre del año base
        semestre_base = 2
    else:  # Si el mes base es julio o antes, empezar en junio del año base
        semestre_base = 1

    for semestre in range(semestre_base, semestre_base + n):

        # Calcular el año y el semestre actual
        año_actual = año_base + (semestre - 1) // 2
        semestre_actual = (semestre - 1) % 2 + 1

        # Determinar el mes de inicio del semestre actual
        mes_inicio_semestre = 1 if semestre_actual == 1 else 12

        # Si la fecha de inicio está después del inicio del semestre, avanzar al siguiente semestre
        if fecha_inicio_dt.month > mes_inicio_semestre:
            semestre += 1
            año_actual = año_base + (semestre - 1) // 2
            semestre_actual = (semestre - 1) % 2 + 1

        # Determinar si el semestre actual es en enero a junio o julio a diciembre
        if semestre_actual == 1:
            fecha_inicio = f"{año_actual}-01-01"
            fecha_corte_str = f"{año_actual}-06-30"
    #        print(f"Calculando para el semestre de enero a junio del año {año_actual}.")
        else:
            fecha_inicio = f"{año_actual}-07-01"
            fecha_corte_str = f"{año_actual}-12-31"
    #        print(f"Calculando para el semestre de julio a diciembre del año {año_actual}.")

        #print(f"buscar tasa en la fecha {fecha_corte_str}.")
        # Obtener la tasa de interés del semestre actual usando la función buscar_tasa_interes
        i_semestral = db.buscar_tasa_interes(fecha_corte_str)
        #print(f"Tasa en la fecha {fecha_corte_str}. = {i_semestral}")

        # Actualizar el valor de D_actual
        D_actual *= (1 + (0.5 * i_semestral/100))
        #print(f"Depósito actual, para la fecha {fecha_corte_str}, con la tasa {i_semestral} = {D_actual}")
        # Agregar el depósito actual a la lista
        depositos_por_semestre.append(D_actual)
    
    # Retornar el último depósito

    if n >= 1:
        ult_deposito = depositos_por_semestre[-2]
        ult_tasa = i_semestral
       # print(f"Ultimo depósito: {ult_deposito} y tasa {ult_tasa}.")
        return ult_deposito, ult_tasa
    
    elif n == 0:
        # Convertir las fechas a objetos datetime si no lo son
        fecha_inicio_dt = fecha_inicio if isinstance(fecha_inicio, datetime) else datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fecha_corte_dt = fecha_corte_str if isinstance(fecha_corte_str, datetime) else datetime.strptime(fecha_corte_str, "%Y-%m-%d")
        
        # Obtener el primer día de cada mes entre fecha_inicio y fecha_corte
        fecha_actual = fecha_inicio_dt
        primeros_dias_meses = []
        while fecha_actual <= fecha_corte_dt:
            primer_dia_mes = datetime(fecha_actual.year, fecha_actual.month, 1)
            primeros_dias_meses.append(primer_dia_mes)
            # Avanzar al primer día del próximo mes
            fecha_actual = primer_dia_mes + timedelta(days=32)
        
        # Obtener la tasa de interés mensual para el primer día de cada mes
        tasas_mensuales = []
        for primer_dia_mes in primeros_dias_meses:
            fecha_str = primer_dia_mes.strftime("%Y-%m-%d")
            i_mensual = db.buscar_tasa_interes(fecha_str)
            if i_mensual is not None:
                tasas_mensuales.append(i_mensual)
        
        # Calcular el promedio de las tasas mensuales
        promedio_tasas_mensuales = sum(tasas_mensuales) / len(tasas_mensuales)
        
        return D_calc, promedio_tasas_mensuales
        #return D, i_fsi
    
    ult_deposito = depositos_por_semestre[-1]
    ult_tasa = i_semestral

    return ult_deposito, ult_tasa
