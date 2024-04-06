from datetime import datetime

def calcular_fraccion_semestre():

    fecha_deposito_str = input("Por favor, ingresa la fecha de depósito (YYYY-MM-DD): ")
    fecha_deposito = datetime.strptime(fecha_deposito_str, '%Y-%m-%d')
    print("fecha_deposito: ",fecha_deposito)
    
    # Obteniendo el año y mes de la fecha de depósito
    year = fecha_deposito.year
    month = fecha_deposito.month
    
    # Definiendo la fecha del próximo semestre
    if month <= 6:  # Si la fecha de depósito es antes de junio, el próximo semestre es junio de este año
        prox_semestre = datetime(year, 6, 30)
    else:  # Si la fecha de depósito es en julio o después, el próximo semestre es diciembre de este año
        prox_semestre = datetime(year, 12, 31)
    
    # Calcular la fracción del semestre
    print(f"t_fsi = ({prox_semestre} - {fecha_deposito}).days = {(prox_semestre - fecha_deposito).days + 1}")
    
    t_fsi = ((prox_semestre - fecha_deposito).days)/ 365
    print(f"t_fsi = {t_fsi}")
    
    return t_fsi

def calcular_deposito_capitalizado(t_sfi_calculado): #Paso 1

    D = float(input("ingresa el monto del depósito inicial (D): "))
    i_fsi = float(input("ingresa la tasa de interés anual como porcentaje para el mes en que se realizo el deposito original en % (i_fsi): "))
    t_fsi = t_sfi_calculado # int(input("ingresa la fracción de semestre en días (t_fsi): "))

    # Convertir la tasa de interés a formato decimal
    i_fsi = i_fsi / 100

    # Calcular el depósito capitalizado
    D_fsi = D * (1 + (i_fsi * (t_fsi)))
    print(f"Depósito capitalizado para la fracción de semestre inicial: {D_fsi:.2f}")

    # Mostrar el resultado
    return D_fsi,i_fsi

def calcular_capitalizacion_por_semestre_interactivo(D_fsi_calculado,i_fsi_paso1): #Paso 2
    # Solicitar al usuario que ingrese los datos necesarios
    n = int(input("Por favor, ingresa el número total de semestres a calcular: "))
    D = D_fsi_calculado #float(input("Por favor, ingresa el monto del depósito inicial (D): "))
    i_fsi = i_fsi_paso1 # float(input("Por favor, ingresa la tasa de interés anual como porcentaje (i_fsi): "))

    D_actual = D
    deposito_por_semestre = [D]  # Incluir el depósito inicial

    i_semestral = i_fsi * 0.5  # Tasa de interés para medio año

    ###Bucle para el calculo de el deposito por cada semestre
    for i in range(1,n + 1):

      if n == 0:
        # Calcular el promedio de las tasas mensuales
        promedio_tasas_mensuales = float(input("Por favor, ingresa la tasa de interés promedio entre los meses comprendidos como porcentaje (i_fsi): "))
        # Actualizar el valor de D_actual
        D_actual *= (1 + (0.5 * promedio_tasas_mensuales/100))
        return D_actual, promedio_tasas_mensuales   

      else:
        # Convertir la tasa de interés anual a una tasa semestral
        i_fsi = float(input("Por favor, ingresa la tasa de interés anual como porcentaje (i_fsi): "))
        i_fsi = i_fsi / 100
        i_semestral = i_fsi * 0.5  # Tasa de interés para medio año
        D_actual *= (1 + i_semestral)
        deposito_por_semestre.append(D_actual)


    for i, deposito in enumerate(deposito_por_semestre):
        print(f"Depósito en el semestre {i}: {deposito:.2f}") 
    
    Deposito_ultimo_semestre = deposito_por_semestre[-1]
    
    return Deposito_ultimo_semestre

def capitalización_depósito_final_semestre(D_ultimo_semestre): #Paso 3
    # Solicitar al usuario que ingrese los datos necesarios
    D = D_ultimo_semestre # float(input("Por favor, ingresa el monto del depósito del ultimo semestre (Dsn): "))
    i_fsi = float(input("Por favor, ingresa la tasa de interés anual como porcentaje del ultimo semestre (i_fsn): "))
    t_fsi = int(input("Por favor, ingresa la fracción de semestre en días (t_fsi): "))

    # Convertir la tasa de interés a formato decimal
    i_fsi = i_fsi / 100

    # Calcular el depósito capitalizado
    D_f = D * (1 + ((t_fsi / 365) * i_fsi))

    # Mostrar el resultado
    return D_f


def SIE():
    t_sfi_calculado = calcular_fraccion_semestre()
    D_fsi_calculado,i_fsi = calcular_deposito_capitalizado(t_sfi_calculado)
    D_ultimo_semestre = calcular_capitalizacion_por_semestre_interactivo(D_fsi_calculado,i_fsi)
    D_final_calculado = capitalización_depósito_final_semestre(D_ultimo_semestre)
    print(f"D_fsi_calculado: {D_fsi_calculado:.2f}\nD_ultimo_semestre: {D_ultimo_semestre:.2f}\nD_final_calculado: {D_final_calculado:.2f}")
    print("SIE terminado")

SIE()