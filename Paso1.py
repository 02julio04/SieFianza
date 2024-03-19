'''
CAPITALIZAR el interés generado durante la fracción de semestre inicial, a razón de
la Tasa de lnteres Anual correspondiente al mes en que se realizó el pago del
depósito:
'''


def calcular_deposito_capitalizado(imp_fian_db,t_fsi_calc,i_fsi_db):
    
    i_fsi = i_fsi_db / 100
    
    # Calcular el depósito capitalizado usando la fórmula de interés compuesto
    D_fsi = imp_fian_db * (1 + (i_fsi * (t_fsi_calc)))
    #print(f"{t_fsi_calc/365}")
    return D_fsi

    
