'''
AGREGAR al depósito capitalizado por la fracción de semestre inicial Dfsi, la
capitalización de los intereses generados para los semestres estándares completos
sucesivos que apliquen
'''

import DB
from datetime import datetime, timedelta
import config

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={config.server};DATABASE={config.database};UID={config.username};PWD={config.password}'
db = DB.Database(conn_str)

def calcular_capitalizacion_por_semestre_interactivo(D_calc, i_fsi_db, semestres, fecha_inicio, fecha_corte_str):
        # Solicitar al usuario que ingrese los datos necesarios
        D = D_calc
        n = semestres

        # Convertir la tasa de interés anual a una tasa semestral
        i_semestral = db.buscar_tasa_interes(fecha_inicio)  # Tasa de interés para medio año        

        D_actual = D
        depositos_por_semestre = [D]
        ult_deposito = 0
        ult_tasa = 0
        
        # Convertir la fecha de inicio a un objeto datetime para manipulación
        fecha_inicio_dt = fecha_inicio if isinstance(
            fecha_inicio, datetime) else datetime.strptime(fecha_inicio, "%Y-%m-%d")
        # Determinar el año y el semestre base
        año_base = fecha_inicio_dt.year
        mes_base = fecha_inicio_dt.month

        # Check if the first interest rate is None and exit if so
        if mes_base > 6:  # Si el mes base es después de junio, empezar en diciembre del año base
            semestre_base = 2
        else:  # Si el mes base es julio o antes, empezar en junio del año base
            semestre_base = 1
        año_limite = 2024
        for semestre in range(semestre_base, semestre_base + n):

            # Calcular el año y el semestre actual
            año_actual = año_base + (semestre - 1) // 2
            semestre_actual = (semestre - 1) % 2 + 1
            if año_actual < año_limite:

                # Determinar el mes de inicio del semestre actual
                mes_inicio_semestre = 1 if semestre_actual == 1 else 7

                # Si la fecha de inicio está después del inicio del semestre, avanzar al siguiente semestre
                if fecha_inicio_dt.month > mes_inicio_semestre:
                    semestre += 1
                    año_actual = año_base + (semestre - 1) // 2
                    semestre_actual = (semestre - 1) % 2 + 1

                # Determinar si el semestre actual es en enero a junio o julio a diciembre
                if semestre_actual == 1:
                    fecha_corte_str = f"{año_actual}-06-30"
                else:
                    fecha_corte_str = f"{año_actual}-12-31"
                    
                # Actualizar el valor de D_actual
                D_actual *= (1 + (0.5 * i_semestral/100))
                print(f"Depósito actual, para la fecha {fecha_corte_str}, con la tasa {i_semestral} = {D_actual}")
                # Agregar el depósito actual a la lista
                depositos_por_semestre.append(D_actual)

                print(f"Buscar tasa en la fecha {fecha_corte_str}.")
                # Obtener la tasa de interés del semestre actual usando la función buscar_tasa_interes
                i_semestral = db.buscar_tasa_interes(fecha_corte_str)
                print(f"Tasa en la fecha {fecha_corte_str} = {i_semestral}")

        # Retornar el último depósito

        if n > 1:
            ult_deposito = depositos_por_semestre[-2]
            ult_tasa = i_semestral
            print(f"Ultimo depósito: {ult_deposito} y tasa {ult_tasa}.")
            return ult_deposito, ult_tasa

        elif n == 0 or n == 1:
            return D_calc, i_fsi_db