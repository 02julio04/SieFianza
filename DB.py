import pyodbc
import datetime
from Enums.Enum_mes import obtener_nombre_mes
import Enums.Enum_mes

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'DAVID\\SQLEXPRESS01'
database = 'DB_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

def Buscar_en_BD():

    #try:
        # Establish connection
    conn = pyodbc.connect(conn_str)

        # Create cursor
    cursor = conn.cursor()

        # Execute SQL queries with square brackets around table name
    cursor.execute('SELECT Top 1 F_RES_CONT FROM [EDE-este]')
    fecha_deposito_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila

    cursor.execute('SELECT Top 1 F_CORTE FROM [EDE-este]')
    fecha_corte_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila

    cursor.execute('SELECT Top 1 IMP_FIAN FROM [EDE-este]')
    imp_fian_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila

    cursor.execute(f"SELECT Top 1 Promedio_Mensual FROM [Promedios] WHERE Mes = {Enums.Enum_mes(int(fecha_deposito_db[5:7])).name} and Año = {obtener_nombre_mes(fecha_corte_db)}")
    i_fsi_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila

    cursor.execute("CREATE TABLE #TablaTemporal (F_CONS_CONT DATETIME, F_CORTE DATETIME, IMP_FIAN FLOAT, i_fsi FLOAT)")    
    cursor.execute(f"INSERT INTO #TablaTemporal (F_CONS_CONT, F_CORTE) VALUES ({fecha_deposito_db}, {fecha_corte_db}, {imp_fian_db}, {i_fsi_db})")
    cursor.execute("SELECT * FROM #TablaTemporal")
    

    for row in cursor.fetchall():
        print(row)
        
        # Close cursor and connection
    cursor.close()
    conn.close()

    
   # except Exception as e:
   #     print(f'Error: {e}')

   #     fecha_deposito_db = None
   #     fecha_corte_db = None

   #     conn.close()
    
    return fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_db