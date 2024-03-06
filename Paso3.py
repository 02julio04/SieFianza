'''
AGREGAR la capitalización del depósito para la fracción final de semestre
'''

def capitalización_depósito_final_semestre():
    # Solicitar al usuario que ingrese los datos necesarios
    D = float(input("Por favor, ingresa el monto del depósito del ultimo semestre (Dsn): "))
    i_fsi = float(input("Por favor, ingresa la tasa de interés anual como porcentaje del ultimo semestre (i_fsn): "))
    t_fsi = int(input("Por favor, ingresa la fracción de semestre en días (t_fsi): "))

    # Convertir la tasa de interés a formato decimal
    i_fsi = i_fsi / 100
    
    # Calcular el depósito capitalizado
    D_f = D * (1 + ((t_fsi / 365) * i_fsi))

    # Mostrar el resultado
    return D_f

# Probar función
print(" AGREGADA la capitalización del depósito para la fracción final de semestre(D_f) es:", capitalización_depósito_final_semestre())





