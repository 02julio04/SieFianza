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

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'DAVID\\SQLEXPRESS01'
database = 'DB_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
db = DB.Database(conn_str)

def SieFianza():
    # Buscar en la BD
    identificador_db,fecha_deposito_str,fecha_corte_str,imp_fian_db = db.buscar_en_bd()
    i_fsi_db = db.buscar_tasa_interes(fecha_deposito_str,fecha_corte_str)
    t_sfi,fecha_deposito,fecha_corte = DeterminaTsfi.calcular_fraccion_semestre(fecha_deposito_str,fecha_corte_str)
    print(f"La fracción del semestre (t_fsi) es: {t_sfi} días,\n la fecha de depósito es: {fecha_deposito},\n la fecha de corte es: {fecha_corte},\n y el importe de la fianza es: {imp_fian_db},\n y la tasa de interés es: {i_fsi_db}")
    # Paso 1
    D_fsi = p1.calcular_deposito_capitalizado(imp_fian_db,t_sfi,i_fsi_db)
    print(f"D_fsi: {D_fsi}")
    # Paso 2
    ult_depo, ult_tasa = p2.calcular_capitalizacion_por_semestre_interactivo(D_fsi,i_fsi_db,Semestres.calcular_semestres(fecha_deposito,fecha_corte),fecha_deposito,fecha_corte_str)
    # Paso 3
    D_f = p3.capitalización_depósito_final_semestre(ult_depo,ult_tasa, fecha_corte_str)
    print(f"El valor final del deposito capitalizado es: {D_f}")
    db.crear_tabla_provicional(identificador_db,fecha_deposito_str,fecha_corte_str,imp_fian_db,i_fsi_db,D_fsi,ult_depo,D_f)
    

SieFianza()
