import pyodbc
import Enums.Enum_mes
import datetime
from tabulate import tabulate

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'DAVID\\SQLEXPRESS01'
database = 'DB_SIE'

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

        cursor.execute("SELECT TOP 10 NIS_RAD FROM [EDE-este] where year(F_RES_CONT) >= 2017")
        identificador_db = cursor.fetchall()

        cursor.execute("SELECT TOP 10 F_RES_CONT FROM [EDE-este] where year(F_RES_CONT) >= 2017")
        fecha_deposito_db = cursor.fetchall()
        
        cursor.execute('SELECT TOP 10 F_CORTE FROM [EDE-este] where year(F_RES_CONT) >= 2017')
        fecha_corte_db = cursor.fetchall()

        cursor.execute('SELECT TOP 10 IMP_FIAN FROM [EDE-este] where year(F_RES_CONT) >= 2017')
        imp_fian_db = cursor.fetchall()

        cursor.close()
        conn.close()

        return identificador_db,fecha_deposito_db, fecha_corte_db, imp_fian_db

    def buscar_tasa_interes(self, fecha_deposito_db):
        conn = self.establish_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT Top 1 Promedio_Mensual FROM [Promedios] WHERE Año >= '{fecha_deposito_db[0:4]}' and Mes = '{Enums.Enum_mes.obtener_nombre_mes(fecha_deposito_db)}'")
        
        # Fetch the result
        result = cursor.fetchone()

        # Check if result is None
        if result is not None:
            i_fsi_db = result[0]
        else:
            # Handle the case where no rows were found
            print("No rows found in the database.")
            i_fsi_db = None  # or any other appropriate value

        cursor.close()
        conn.close()

        return i_fsi_db
    
    def crear_tabla_provicional(self, identificador_db, fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list):
        conn = self.establish_connection()
        cursor = conn.cursor()

        # Crear la tabla temporal una vez fuera del bucle
        cursor.execute("CREATE TABLE #temp (NIS_RAD FLOAT, F_RES_CONT DATE, F_CORTE DATE, IMP_FIAN FLOAT, Promedio_Mensual FLOAT, D_fsi FLOAT, Deposito_Ultimo_semestre FLOAT, D_f FLOAT)")

        # Iterar sobre las listas y realizar la inserción de datos en la tabla temporal
        for identificador, fecha_deposito_2, fecha_corte_2, imp_fian_2, i_fsi, d_fsi, u_depo, d_f in zip(identificador_db, fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_list, D_fsi_list, ult_depo_list, D_f_list):
            identificador_ = identificador.NIS_RAD
            fecha_deposito_c = fecha_deposito_2.F_RES_CONT
            fecha_corte_c = fecha_corte_2.F_CORTE
            imp_fian_3 = imp_fian_2.IMP_FIAN

            # Insertar datos en la tabla temporal
            cursor.execute("INSERT INTO #temp (NIS_RAD, F_RES_CONT, F_CORTE, IMP_FIAN, Promedio_Mensual, D_fsi, Deposito_Ultimo_semestre, D_f) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (identificador_, fecha_deposito_c, fecha_corte_c, imp_fian_3, i_fsi, d_fsi, u_depo, d_f))

        # Imprimir la tabla temporal usando tabulate
        cursor.execute("SELECT * FROM #temp")
        rows = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        print(tabulate(rows, headers=headers, tablefmt="grid"))

        cursor.close()
        conn.close()

