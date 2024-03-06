'''
AGREGAR al depósito capitalizado por la fracción de semestre inicial Dfsi, la
capitalización de los intereses generados para los semestres estándares completos
sucesivos que apliquen
'''

def calcular_capitalizacion_por_semestre_interactivo():
    # Solicitar al usuario que ingrese los datos necesarios
    D = float(input("Por favor, ingresa el monto del depósito inicial (D): "))
    i_fsi = float(input("Por favor, ingresa la tasa de interés anual como porcentaje (i_fsi): "))
    n = int(input("Por favor, ingresa el número total de semestres a calcular: "))

    # Convertir la tasa de interés anual a una tasa semestral
    i_fsi = i_fsi / 100
    i_semestral = i_fsi * 0.5  # Tasa de interés para medio año

    # Inicializar el depósito capitalizado con el valor inicial para la fracción del primer semestre
    D_actual = D
    depositos_por_semestre = [D]  # Incluir el depósito inicial

    # Aplicar la capitalización para cada semestre hasta n
    for _ in range(1, n+1):
        D_actual *= (1 + i_semestral)
        depositos_por_semestre.append(D_actual)
    
    # Mostrar el resultado para cada semestre
    for i, deposito in enumerate(depositos_por_semestre):
        print(f"Semestre {i}: {deposito:.2f}")

calcular_capitalizacion_por_semestre_interactivo()