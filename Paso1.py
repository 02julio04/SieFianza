'''
CAPITALIZAR el interés generado durante la fracción de semestre inicial, a razón de
la Tasa de lnteres Anual correspondiente al mes en que se realizó el pago del
depósito:
'''


def calcular_deposito_capitalizado(imp_fian_db,t_fsi_calc,i_fsi_db):
    
    D = imp_fian_db #float(input("ingresa el monto del depósito inicial (D): "))
    i_fsi = i_fsi_db #float(input("ingresa la tasa de interés anual como porcentaje (i_fsi): "))
    t_fsi = t_fsi_calc #int(input("ingresa la fracción de semestre en días (t_fsi): "))
    
    # Convertir la tasa de interés a formato decimal
    i_fsi = i_fsi / 100
    
    # Calcular el depósito capitalizado
    D_fsi = D * (1 + (i_fsi * (t_fsi / 365)))
    
    # Mostrar el resultado
    return D_fsi

