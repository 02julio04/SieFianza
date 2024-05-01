'''
CAPITALIZAR el interés generado durante la fracción de semestre inicial, a razón de
la Tasa de lnteres Anual correspondiente al mes en que se realizó el pago del
depósito:
'''
import DB
from datetime import datetime, timedelta
import config
# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={config.server};DATABASE={config.database};UID={config.username};PWD={config.password}'
db = DB.Database(conn_str) 
def calcular_deposito_capitalizado(imp_fian_db,t_fsi_calc,i_fsi_db,fecha_inicio,fecha_corte_str):

    # Obtener la fecha de contrato actual
    fecha_contrato = fecha_inicio
    fecha_corte = fecha_corte_str
    
    i_fsi = i_fsi_db
    t_fsi = t_fsi_calc
    
    # Convertir la tasa de interés a formato decimal
    i_fsi = i_fsi / 100

        # Calcular el depósito capitalizado
    D_fsi = imp_fian_db * (1 + (i_fsi * (t_fsi)))

        # Actualizar la fecha de contrato al próximo semestre
      #  if (fecha_contrato.month < 7 and fecha_corte.month < 7) or (fecha_contrato.month > 6 and fecha_corte.month > 6):
      #      pass
    if fecha_contrato.month > 6:
        fecha_contrato = fecha_contrato.replace(month=12,day=1)
    else:
        fecha_contrato = fecha_contrato.replace(month=6,day=1)
        # Mostrar el resultado
    return D_fsi, i_fsi*100, fecha_contrato.strftime('%Y-%m-%d')

    
