'''
AGREGAR la capitalización del depósito para la fracción final de semestre
'''
from datetime import datetime
import DB
from datetime import datetime, timedelta
import config

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={config.server};DATABASE={config.database};UID={config.username};PWD={config.password}'
db = DB.Database(conn_str)


def capitalización_depósito_final_semestre(D_ultimo_semestre, ult_tasa, fecha_corte,semestres):
    if semestres == 0:
        return D_ultimo_semestre
    else:
        # Solicitar al usuario que ingrese los datos necesarios
        D = D_ultimo_semestre

        fecha_corte_original = fecha_corte

        # Determinar el año y el semestre del último semestre
        año_ultimo_semestre = fecha_corte_original.year - \
            1 if fecha_corte_original.month < 7 else fecha_corte_original.year
        ultimo_semestre = datetime(año_ultimo_semestre, 12, 31) if fecha_corte_original.month < 7 else datetime(
            año_ultimo_semestre, 6, 30)

        print(f"Fecha de corte original: {fecha_corte_original}")
        print(f"Último semestre: {ultimo_semestre}")
        print(f"Días restantes: {
            (fecha_corte_original - ultimo_semestre).days}")
        fraccion_dias_restantes = (fecha_corte_original - ultimo_semestre).days
        t_fsi = fraccion_dias_restantes

        # Convertir la tasa de interés a formato decimal
        i_fsi = db.buscar_tasa_interes(str(ultimo_semestre)[:9]) / 100
        D = float(D[0]) if isinstance(D, tuple) else float(D)
        # Calcular el depósito capitalizado
        D_f = D * (1 + ((t_fsi / 365) * i_fsi))
        # Mostrar el resultado
        return D_f






