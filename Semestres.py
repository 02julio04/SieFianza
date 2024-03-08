from datetime import datetime

def calcular_semestres(fecha_inicio, fecha_fin):
    # Definir la duración de un semestre en días
    dias_por_semestre = 365 / 2
    
    # Calcular la diferencia en días entre las dos fechas
    diferencia_dias = (fecha_fin - fecha_inicio).days
    
    # Calcular la cantidad de semestres redondeando hacia abajo
    cantidad_semestres = int(diferencia_dias / dias_por_semestre)
    
    return cantidad_semestres

# fecha_inicio = datetime(2000, 1, 1)  # Ejemplo de fecha de inicio
# fecha_fin = datetime(2020, 11, 13)    # Ejemplo de fecha de fin

# Calcular la cantidad de semestres entre las dos fechas
# cantidad_semestres = calcular_semestres(fecha_inicio, fecha_fin)

# print("Cantidad de semestres:", cantidad_semestres)