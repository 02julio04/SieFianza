import pyodbc

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'DAVID\\SQLEXPRESS01'
database = 'DB_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'

def Buscar_en_BD():
    # Establish connection
    conn = pyodbc.connect(conn_str)

    # Create cursor
    cursor = conn.cursor()

    # Execute SQL queries with square brackets around table name
    cursor.execute('SELECT Top 1 F_RES_CONT FROM [EDE-este]')
    fecha_deposito_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila

    cursor.execute('SELECT Top 1 F_CORTE FROM [EDE-este]')
    fecha_corte_db = cursor.fetchone()[0]  # Obteniendo el primer valor de la primera fila
    
    # Close cursor and connection
    cursor.close()
    conn.close()
    
    return fecha_deposito_db, fecha_corte_db