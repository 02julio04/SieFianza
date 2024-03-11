import pyodbc
import Enums.Enum_mes

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

        cursor.execute('SELECT Top 1 F_RES_CONT FROM [EDE-este]')
        fecha_deposito_db = cursor.fetchone()[0]

        cursor.execute('SELECT Top 1 F_CORTE FROM [EDE-este]')
        fecha_corte_db = cursor.fetchone()[0]

        cursor.execute('SELECT Top 1 IMP_FIAN FROM [EDE-este]')
        imp_fian_db = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return fecha_deposito_db, fecha_corte_db, imp_fian_db

    def buscar_tasa_interes(self, fecha_deposito_db, fecha_corte_db):
        conn = self.establish_connection()
        cursor = conn.cursor()

        cursor.execute(f"SELECT Top 1 Promedio_Mensual FROM [Promedios] WHERE Mes = {Enums.Enum_mes(int(fecha_deposito_db[5:7])).name} and Año = {Enums.Enum_mes.obtener_nombre_mes(fecha_corte_db)}")
        i_fsi_db = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return i_fsi_db