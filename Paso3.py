'''
AGREGAR la capitalización del depósito para la fracción final de semestre
'''
from datetime import datetime


def capitalización_depósito_final_semestre(ult_deposito, ult_tasa, fecha_corte,cantidad_semestres):
    if cantidad_semestres == 0:
        return ult_deposito
    else:
        D = ult_deposito 
        i_fsi =  ult_tasa 

        # Assume fecha_corte could be a datetime object or a string
        if isinstance(fecha_corte, datetime):
            fecha_corte_original = fecha_corte
        elif isinstance(fecha_corte, str):
            fecha_corte_original = datetime.strptime(fecha_corte, "%Y-%m-%d")
        else:
            # Handle other types or raise an error
            raise TypeError("fecha_corte must be a datetime object or a string representing a date")
        
        # Determinar el año y el semestre del último semestre
        año_ultimo_semestre = fecha_corte_original.year if fecha_corte_original.month < 7 else fecha_corte_original.year
        ultimo_semestre = datetime(año_ultimo_semestre, 1, 1) if fecha_corte_original.month < 7 else datetime(año_ultimo_semestre, 7, 1)

        fraccion_dias_restantes = (fecha_corte_original - ultimo_semestre).days
        t_fsi =  fraccion_dias_restantes # int(input("Por favor, ingresa la fracción de semestre en días (t_fsi): "))

        # Convertir la tasa de interés a formato decimal
        i_fsi = i_fsi / 100
        D = float(D[0]) if isinstance(D, tuple) else float(D)
        # Calcular el depósito capitalizado
        D_f = D * (1 + ((t_fsi / 365) * i_fsi))
        print(f"Ult Depósito (Received): {ult_deposito}")
        print(f"Tasa (Received): {ult_tasa}")
        print(f"Fecha Corte (Processed): {fecha_corte_original}")
        print(f"Días Restantes: {fraccion_dias_restantes}")
        print(f"D_f Calculated: {D_f}")
        print("----------------------")

        # Mostrar el resultado
        return D_f






