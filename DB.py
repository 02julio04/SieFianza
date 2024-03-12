import pyodbc
import Enums.Enum_mes
import datetime

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

        cursor.execute("SELECT Top 1 F_RES_CONT FROM [EDE-este] WHERE NIS_RAD = 4125422")
        fecha_deposito_db = cursor.fetchone()[0]

        cursor.execute('SELECT Top 1 F_CORTE FROM [EDE-este] WHERE NIS_RAD = 4125422')
        fecha_corte_db = cursor.fetchone()[0]

        cursor.execute('SELECT Top 1 IMP_FIAN FROM [EDE-este] WHERE NIS_RAD = 4125422')
        imp_fian_db = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return fecha_deposito_db, fecha_corte_db, imp_fian_db

    def buscar_tasa_interes(self, fecha_deposito_db, fecha_corte_db):
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