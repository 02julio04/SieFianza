'''
PARA CALCULAR EL VALOR ACTUALIZADO DE LA FIANZA
CASO: CONSTITUCIÓN DE FIANZA MEDIANTE DEPÓSITO ÚNICO
'''
import DB
import DeterminaTsfi
import Semestres
import Paso1 as p1
import Paso2 as p2
import Paso3 as p3
import csv
import datetime
import pyodbc

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'PEDROJULIO'
database = 'Db_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
db = DB.Database(conn_str)  # Create a new instance


def SieFianza(empresa_input):
    # empresa_input = input("De qué empresa quieres obtener los datos (EDEESTE, EDESUR, EDENORTE): ")
    i_fsi_list = []
    t_sfi_list = []
    D_fsi_list = []
    ult_depo_list = []
    ult_tasa_list =  []
    semestres_list = []
    D_fsi_list = []
    D_f_list = []
    # Buscar en la BD
    empresa_db,identificador_db,fecha_deposito_str,fecha_corte_str,imp_fian_db = db.buscar_en_bd(empresa_input)

    for row in fecha_deposito_str:  # Suponiendo que rows contiene los resultados de la consulta a la base de datos
        fecha = row.F_RES_CONT  # Reemplaza "fecha_columna" con el nombre real de la columna de fecha
        i_fsi_db = db.buscar_tasa_interes(fecha)
        i_fsi_list.append(i_fsi_db)

    for fecha_deposito, fecha_corte in zip(fecha_deposito_str, fecha_corte_str):
     # Calcular la fracción del semestre para cada par de fechas
        fecha_deposito_ = fecha_deposito.F_RES_CONT
        fecha_corte_ = fecha_corte.F_CORTE
        t_sfi = DeterminaTsfi.calcular_fraccion_semestre(fecha_deposito_, fecha_corte_)
        t_sfi_list.append(t_sfi)
        semestres = Semestres.calcular_semestres(fecha_deposito_,fecha_corte_)
        semestres_list.append(semestres)
   
    # Paso 1
    for imp_fian, t_sfi_, i_fsi_ in zip(imp_fian_db, t_sfi_list, i_fsi_list):
        imp_fian_ = imp_fian.IMP_FIAN
        D_fsi = p1.calcular_deposito_capitalizado(imp_fian_,t_sfi_,i_fsi_)
        #print(f"D_fsi = {D_fsi}")
        D_fsi_list.append(D_fsi)
    
    # Paso 2
    for fecha_deposito_2, fecha_corte_2, D_fsi_, i_fsi_, semestres_ in zip(fecha_deposito_str, fecha_corte_str, D_fsi_list, i_fsi_list, semestres_list): 
        fecha_deposito_a = fecha_deposito_2.F_RES_CONT
        fecha_corte_a = fecha_corte_2.F_CORTE
        ult_depo, ult_tasa = p2.calcular_capitalizacion_por_semestre_interactivo(D_fsi_, i_fsi_, semestres_, fecha_deposito_a,fecha_corte_a)
        ult_depo_list.append(ult_depo)
        ult_tasa_list.append(ult_tasa)

    # Paso 3
    for fecha_corte_3, ult_depo, ult_tasa in zip(fecha_corte_str, ult_depo_list, ult_tasa_list):
        fecha_corte_b = fecha_corte_3.F_CORTE
        D_f = p3.capitalización_depósito_final_semestre(ult_depo,ult_tasa, fecha_corte_b)
        D_f_list.append(D_f)
        
    # Crear tabla provisional
    db.crear_tabla_provicional(empresa_db,identificador_db,fecha_deposito_str, fecha_corte_str, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list)
    

    # Save results to a file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        # Write headers
        writer.writerow(['Empresa','Identificador', 'Fecha Deposito', 'Fecha Corte', 'Importe Fianza', 'Interes', 'D_fsi', 'Ultimo Deposito', 'Ultima Tasa', 'D_f'])
        
        # Write data
        for data in zip(empresa_db,identificador_db, fecha_deposito_str, fecha_corte_str, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, ult_tasa_list, D_f_list):
            empresa = data[0][0] if isinstance(data[0], pyodbc.Row) else data[0]
            identificador = data[1][0] if isinstance(data[1], pyodbc.Row) else data[1]
            fecha_deposito = data[2][0] if isinstance(data[2], pyodbc.Row) else data[2]
            fecha_corte = data[3][0] if isinstance(data[3], pyodbc.Row) else data[3]
            importe = data[4][0] if isinstance(data[4], pyodbc.Row) else data[4]
            formatted_fecha_deposito = fecha_deposito.strftime('%Y-%m-%d') if isinstance(fecha_deposito, datetime.datetime) else fecha_deposito
            formatted_fecha_corte = fecha_corte.strftime('%Y-%m-%d') if isinstance(fecha_corte, datetime.datetime) else fecha_corte
            
            # Round the numeric values and write the new data to the file
            new_data = [
                empresa,  # Empresa
                identificador,  # Identificador
                formatted_fecha_deposito,  # Fecha Deposito
                formatted_fecha_corte, # Fecha Corte
                importe
            ] + [round(value, 4) if isinstance(value, (int, float)) else value for value in data[5:]]  # Rest of data
            
            writer.writerow(new_data)
    return list(zip(empresa_db, identificador_db, fecha_deposito_str, fecha_corte_str, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list))

