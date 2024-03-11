'''
AGREGAR al depósito capitalizado por la fracción de semestre inicial Dfsi, la
capitalización de los intereses generados para los semestres estándares completos
sucesivos que apliquen
'''

def calcular_capitalizacion_por_semestre_interactivo(D_calc,i_fsi_db,semestres): #fecha_deposito,#fecha_corte
    # Solicitar al usuario que ingrese los datos necesarios
    D = D_calc # float(input("Por favor, ingresa el monto del depósito inicial (D): "))
    i_fsi = i_fsi_db # float(input("Por favor, ingresa la tasa de interés anual como porcentaje (i_fsi): "))
    n = semestres # int(input("Por favor, ingresa el número total de semestres a calcular: "))

    # Convertir la tasa de interés anual a una tasa semestral
    i_fsi = i_fsi / 100
    i_semestral = i_fsi * 0.5  # Tasa de interés para medio año

    # Inicializar el depósito capitalizado con el valor inicial para la fracción del primer semestre
    D_actual = D
    depositos_por_semestre = [D]  # Incluir el depósito inicial

    # Idea: búsqueda de tasa de interés en la base de datos para cada semestre
    # Usar una bandera que sea False cuando esté en el semestre de diciembre
    # y cambie a True cuando se mueva al próximo semestre (el loop del cálculo de los semestres cambie de iteración)
    # y así buscar la tasa de interés en la base de datos para el próximo semestre

    # Hacer que i_semestral sea una lista con todos los valores de la tasa de interés para cada semestre( Esta es supuestamente mas eficiente, crer una nueva funcion)

    # Aplicar la capitalización para cada semestre hasta n 
    for _ in range(1, n+1):
        D_actual *= (1 + i_semestral)
        depositos_por_semestre.append(D_actual)
    
    # Mostrar el resultado para cada semestre
    for i, deposito in enumerate(depositos_por_semestre):
        print(f"Semestre {i}: {deposito:.2f}")

    # Para retornar el ultimo valor de la lista
    ult_deposito = depositos_por_semestre[-1]

    return ult_deposito

# calcular_capitalizacion_por_semestre_interactivo()