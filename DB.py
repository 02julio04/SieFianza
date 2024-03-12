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

        cursor.execute("SELECT NIS_RAD FROM [EDE-este] where year(F_RES_CONT) >= 2017")
        identificador_db = cursor.fetchall()

        cursor.execute("SELECT F_RES_CONT FROM [EDE-este] where year(F_RES_CONT) >= 2017")
        fecha_deposito_db = cursor.fetchall()
        
        cursor.execute('SELECT F_CORTE FROM [EDE-este] where year(F_RES_CONT) >= 2017')
        fecha_corte_db = cursor.fetchall()

        cursor.execute('SELECT IMP_FIAN FROM [EDE-este] where year(F_RES_CONT) >= 2017')
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
    
    def crear_tabla_provicional(self,identificador,fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_db, D_fsi,ult_depo,D_f):
      #  conn = self.establish_connection()
      #  cursor = conn.cursor()
      #  cursor.execute("CREATE TABLE #temp (NIS_RAD INT, F_RES_CONT DATE, F_CORTE DATE, IMP_FIAN FLOAT, Promedio_Mensual FLOAT, D_fsi FLOAT, Deposito_Ultimo_semestre FLOAT, D_f FLOAT)")

        # Insertar datos en la tabla temporal
      # cursor.execute("INSERT INTO #temp (NIS_RAD, F_RES_CONT, F_CORTE, IMP_FIAN, Promedio_Mensual,D_fsi,Deposito_Ultimo_semestre,D_f) VALUES (?, ?, ?, ?, ?,?, ?, ?)", 
      #                 (identificador, fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_db, f"{D_fsi:.2f}", f"{ult_depo:.2f}", f"{D_f:.2f}"))

        # Imprimir la tabla temporal usando tabulate
      #  cursor.execute("SELECT * FROM #temp")
      #  rows = cursor.fetchall()
      #  headers = [column[0] for column in cursor.description]
      #  print(tabulate(rows, headers=headers, tablefmt="grid"))

      #  cursor.close()
      #  conn.close()
        conn = self.establish_connection()
        cursor = conn.cursor()

      #  cursor.execute("CREATE TABLE #temp (NIS_RAD INT, F_RES_CONT DATE, F_CORTE DATE, IMP_FIAN FLOAT, Promedio_Mensual FLOAT, D_fsi FLOAT, Deposito_Ultimo_semestre FLOAT, D_f FLOAT)")
        
        # Asegurarse de que todas las listas tengan la misma longitud
      #  assert len(fecha_deposito_db) == len(fecha_corte_db) == len(imp_fian_db) == len(i_fsi_db) == len(D_fsi) == len(ult_depo) == len(D_f), "Las listas deben tener la misma longitud"
        print(f"Longitud de Fecha deposito: {len(fecha_deposito_db)}")
        print(f"Longitud de Fecha de corte:{len(fecha_corte_db)}")
        print(f"Longitud de Deposito inicial:{len(imp_fian_db)}")
        print(f"Longitud de i_fsi:{len(i_fsi_db)}")
        print(f"Longitud de D_fsi:{len(D_fsi)}")
        print(f"Longitud de Ult_deposito:{len(ult_depo)}")
        print(f"Longitud de D_f:{len(D_f)}")
        # Iterar sobre las listas y realizar la inserción de datos en la tabla temporal
     #   for fecha_deposito, fecha_corte, imp_fian, i_fsi, d_fsi, u_depo, d_f in zip(fecha_deposito_db, fecha_corte_db, imp_fian_db, i_fsi_db, D_fsi, ult_depo, D_f):
     #       cursor.execute("INSERT INTO #temp (NIS_RAD, F_RES_CONT, F_CORTE, IMP_FIAN, Promedio_Mensual, D_fsi, Deposito_Ultimo_semestre, D_f) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
     #                   (identificador, fecha_deposito, fecha_corte, imp_fian, i_fsi, d_fsi, u_depo, d_f))

        # Imprimir la tabla temporal usando tabulate
     #   cursor.execute("SELECT * FROM #temp")
     #   rows = cursor.fetchall()
     #   headers = [column[0] for column in cursor.description]
     #   print(tabulate(rows, headers=headers, tablefmt="grid"))

        cursor.close()
        conn.close()

