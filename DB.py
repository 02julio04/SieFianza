import pyodbc
import Enums.Enum_mes
from datetime import datetime
from tabulate import tabulate

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'PEDROJULIO'
database = 'Db_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

class Database:

    def __init__(self, conn_str):
        self.conn_str = conn_str

    def establish_connection(self):
        return pyodbc.connect(self.conn_str)

    def buscar_en_bd(self):
        conn = self.establish_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT TOP 1000 EMPRESA FROM [EDES] WHERE YEAR(F_RES_CONT) >= 2017")
        empresa_db = cursor.fetchall()

        cursor.execute("SELECT TOP 1000 NIS_RAD FROM [EDES] WHERE YEAR(F_RES_CONT) >= 2017")
        identificador_db = cursor.fetchall()

        cursor.execute("SELECT TOP 1000 F_RES_CONT FROM [EDES] WHERE YEAR(F_RES_CONT) >= 2017")
        fecha_deposito_db = cursor.fetchall()
        
        cursor.execute("SELECT TOP 1000 F_CORTE FROM [EDES] WHERE YEAR(F_RES_CONT) >= 2017")
        fecha_corte_db = cursor.fetchall()

        cursor.execute("SELECT TOP 1000 IMP_FIAN FROM [EDES] WHERE YEAR(F_RES_CONT) >= 2017")
        imp_fian_db = cursor.fetchall()

        cursor.close()
        conn.close()

        return empresa_db,identificador_db,fecha_deposito_db, fecha_corte_db, imp_fian_db

    def buscar_tasa_interes(self, fecha_deposito_db):
        conn = self.establish_connection()
        cursor = conn.cursor()
        if isinstance(fecha_deposito_db, str):
    # It's a string, so parse it to a datetime object
            date_format = "%Y-%m-%d"  # Adjust this format to match the actual date format
            fecha_deposito_date = datetime.strptime(fecha_deposito_db, date_format)
        else:
    # It's already a datetime object, no need to parse it
             fecha_deposito_date = fecha_deposito_db
        # Now you can access the 'year' attribute
        año_deposito = fecha_deposito_date.year
        mes_nombres = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        nombre_mes = mes_nombres[fecha_deposito_date.month - 1]  # Obtén el nombre del mes en español  # o "%m" si necesitas el número del mes

        cursor.execute(f"""
        SELECT Promedio_Mensual
        FROM [InteresMensual]
        WHERE Año >= {año_deposito}
        AND Mes = '{nombre_mes}'
        AND Promedio_Mensual IS NOT NULL
        """)
        #print(f"Year: {año_deposito}, Month: {nombre_mes}")
        #print(f"Executing query: SELECT Top 1 Promedio_Mensual FROM [InteresMensual] WHERE Año >= '{año_deposito}' and Mes = '{nombre_mes}'")

        # Fetch the result
        result = cursor.fetchone()

        # Check if result is None
        if result is not None:
            i_fsi_db = result[0]
        else:
             # Handle the case where no rows were found
            print(f"No rows found in the database. in {año_deposito}, {nombre_mes}.")
            i_fsi_db = None  # or any other appropriate value

        cursor.close()
        conn.close()

        return i_fsi_db
    
    def crear_tabla_provicional(self, empresa_db,identificador_db, fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list):
        conn = self.establish_connection()
        cursor = conn.cursor()

        # Crear la tabla temporal una vez fuera del bucle
        cursor.execute("CREATE TABLE #temp (EMPRESA VARCHAR(100), NIS_RAD FLOAT, F_RES_CONT DATE, F_CORTE DATE, IMP_FIAN FLOAT, Promedio_Mensual FLOAT, D_fsi FLOAT, Deposito_Ultimo_semestre FLOAT, D_f FLOAT)")

        # Iterar sobre las listas y realizar la inserción de datos en la tabla temporal
        for empresa, identificador, fecha_deposito_2, fecha_corte_2, imp_fian_2, i_fsi, d_fsi, u_depo, d_f in zip(empresa_db,identificador_db, fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list):
            empresa_name = empresa[0]
            identificador_ = identificador.NIS_RAD
            fecha_deposito_c = fecha_deposito_2.F_RES_CONT
            fecha_corte_c = fecha_corte_2.F_CORTE
            imp_fian_3 = imp_fian_2.IMP_FIAN

            # Insertar datos en la tabla temporal
            cursor.execute("INSERT INTO #temp (EMPRESA, NIS_RAD, F_RES_CONT, F_CORTE, IMP_FIAN, Promedio_Mensual, D_fsi, Deposito_Ultimo_semestre, D_f) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)",
                            (empresa_name, identificador_, fecha_deposito_c, fecha_corte_c, imp_fian_3, i_fsi, d_fsi, u_depo, d_f))

        # Imprimir la tabla temporal usando tabulate
        cursor.execute("SELECT * FROM #temp")
        rows = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

        cursor.close()
        conn.close()

