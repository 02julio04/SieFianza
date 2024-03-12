from datetime import datetime

def calcular_semestres(fecha_inicio, fecha_fin):
    # Definir la duración de un semestre en días
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    dias_por_semestre = 365 / 2
    
    # Calcular la diferencia en días entre las dos fechas
    diferencia_dias = (fecha_fin - fecha_inicio).days
    
    # Calcular la cantidad de semestres redondeando hacia abajo
    cantidad_semestres = int(diferencia_dias / dias_por_semestre)
    
    return cantidad_semestres
