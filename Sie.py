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


def SieFianza():
    
    # Buscar en la BD
    fecha_deposito_str,fecha_corte_str,imp_fian_db = DB.Database.buscar_en_bd()
    i_fsi_db = DB.Database.buscar_tasa_interes(fecha_deposito_str,fecha_corte_str)
    t_sfi,fecha_deposito,fecha_corte = DeterminaTsfi.calcular_fraccion_semestre(fecha_deposito,fecha_corte)
    # Paso 1
    p1.Paso1.calcular_deposito_capitalizado(imp_fian_db,t_sfi,i_fsi_db)
    # Paso 2
    ult_depo = p2.Paso2(imp_fian_db,i_fsi_db,Semestres.calcular_semestres(fecha_deposito_str,fecha_corte_str))
    # Paso 3
    p3.Paso3(ult_depo)
