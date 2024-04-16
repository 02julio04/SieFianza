from datetime import datetime

def calcular_semestres(fecha_inicio, fecha_fin):
    
    # Calcular el año de inicio y fin
    ano_inicio = fecha_inicio.year
    ano_fin = fecha_fin.year

    # Calcular los semestres de inicio y fin
    semestre_inicio = 1 if fecha_inicio.month <= 6 else 2
    semestre_fin = 1 if fecha_fin.month <= 6 else 2

   # Calcular la cantidad de semestres redondeando hacia abajo
    cantidad_semestres = (ano_fin - ano_inicio) * 2 + \
            semestre_fin - semestre_inicio

    # Si la fecha de fin está dentro del segundo semestre y no es el final del semestre, sumamos 1
    if fecha_fin.month > 6 and fecha_fin.day > 30:
        cantidad_semestres += 1

    return cantidad_semestres

