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
import tkinter as tk
from tkinter import ttk, PhotoImage
import decimal

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
    for imp_fian,fecha_deposito_2,fecha_corte_2, t_sfi_, i_fsi_ in zip(imp_fian_db,fecha_deposito_str,fecha_corte_str, t_sfi_list, i_fsi_list):
        imp_fian_ = imp_fian.IMP_FIAN
        fecha_deposito_a = fecha_deposito_2.F_RES_CONT
        fecha_corte_a = fecha_corte_2.F_CORTE
        D_fsi, i_x, it = p1.calcular_deposito_capitalizado(imp_fian_,t_sfi_,i_fsi_,fecha_deposito_a,fecha_corte_a)
        #print(f"D_fsi = {D_fsi}")
        D_fsi_list.append(D_fsi)
    
    # Paso 2
    for fecha_deposito_2, fecha_corte_2, D_fsi_, i_fsi_, cantidad_semestres in zip(fecha_deposito_str, fecha_corte_str, D_fsi_list, i_fsi_list, semestres_list): 
        fecha_deposito_a = fecha_deposito_2.F_RES_CONT
        fecha_corte_a = fecha_corte_2.F_CORTE
        ult_depo, ult_tasa = p2.calcular_capitalizacion_por_semestre_interactivo(D_fsi_, i_fsi_, cantidad_semestres, fecha_deposito_a,fecha_corte_a)
        ult_depo_list.append(ult_depo)
        ult_tasa_list.append(ult_tasa)

    # Paso 3
    for fecha_corte_3, ult_depo, ult_tasa,cantidad_semestres in zip(fecha_corte_str, ult_depo_list, ult_tasa_list,semestres_list):
        fecha_corte_b = fecha_corte_3.F_CORTE
        D_f = p3.capitalización_depósito_final_semestre(ult_depo,ult_tasa, fecha_corte_b,cantidad_semestres)
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

# Esta función actualiza la interfaz gráfica con los datos
def format_fecha(value):
    """Formatea la fecha para mostrar en la GUI."""
    # Si es una instancia de pyodbc.Row, extrae el valor de fecha.
    if isinstance(value, pyodbc.Row) and len(value) > 0:
        value = value[0]
    # Ahora verifica si es un objeto datetime y formatea.
    if isinstance(value, datetime.datetime):
        return value.strftime('%Y-%m-%d')
    return value

def format_numero(value):
    # Si el valor es una instancia de pyodbc.Row, extrae el primer elemento.
    if isinstance(value, pyodbc.Row):
        value = value[0] if value else None
    """Formatea el número para mostrar en la GUI."""
    if isinstance(value, (int, float, decimal.Decimal)):
        return f"{value:.2f}"
    return value

def update_gui_with_data(tree):
    # Aquí llamarías a SieFianza o cualquier otra función que obtenga los datos
    # Reemplazar con el valor obtenido de la entrada del usuario en la GUI
    empresa_input = empresa_entry.get().upper() 
    rows = SieFianza(empresa_input)
    
    # Primero limpia el árbol
    tree.delete(*tree.get_children())

    # Inserta los nuevos datos
    for row in rows:
        # Aplica la formateación a cada valor de la fila antes de insertarlo
        formatted_row = [format_numero(row[0]), (row[1]), format_fecha(row[2]), format_fecha(row[3]), format_numero(row[4]), (row[5]), format_numero(row[6]), format_numero(row[7]), format_numero(row[8])]
        tree.insert('', 'end', values=formatted_row, tags=('lineTag',))

# Configuración inicial de la ventana y el Treeview
# Define los colores y estilos
COLOR_FONDO = "#e1d8b2"
COLOR_BOTON = "#8aa2a9"
COLOR_TEXTO = "#333333"
FUENTE = ("Arial", 16)
FUENTE_TITULO = ("Arial", 18, "bold")

root = tk.Tk()
root.title("Calculadora de Depósito de Fianza")

# Cargar la imagen
image_path = 'logo_sie.png'  # Asegúrate de tener la ruta correcta a la imagen
logo_image  = PhotoImage(file=image_path)

# Cambia los valores de 'x' y 'y' para ajustar el nuevo tamaño
small_logo = logo_image.subsample(2, 2)  # Reduce a la mitad la imagen

# Configura el color de fondo de la ventana
root.configure(bg=COLOR_FONDO)

# Crea el frame de entrada
frame_entrada = tk.Frame(root, bg=COLOR_FONDO)
frame_entrada.pack(side='top', fill='x', pady=(5, 0), padx=10)

# Posiciona la imagen en el lado izquierdo
logo_label = tk.Label(frame_entrada, image=small_logo, bg=COLOR_FONDO)
logo_label.image = small_logo
logo_label.grid(row=0, column=0, padx=(0, 20))

# Posiciona la etiqueta "Empresa:" al lado de la imagen
empresa_label = tk.Label(frame_entrada, text="Empresa:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE)
empresa_label.grid(row=0, column=1, sticky='e')

# Posiciona el campo de entrada al lado de la etiqueta "Empresa:"
empresa_entry = tk.Entry(frame_entrada, font=FUENTE)
empresa_entry.grid(row=0, column=2, sticky='we')

# Configura la expansión de las columnas para alinear los elementos
frame_entrada.columnconfigure(2, weight=1)

# Botón para obtener los datos y actualizar la GUI
# Funciones para cambiar el estilo del botón con hover
def on_enter(e):
    btn_obtener_datos['background'] = 'white'  # Un color más claro para el hover

def on_leave(e):
    btn_obtener_datos['background'] = COLOR_BOTON  # El color original del botón

# Configura el botón 'Obtener Datos' con eventos de hover
btn_obtener_datos = tk.Button(frame_entrada, text='Obtener Datos', font=FUENTE, bg=COLOR_BOTON, fg=COLOR_TEXTO, command=lambda: update_gui_with_data(tree))
btn_obtener_datos.grid(row=0, column=3, padx=(20, 0))

# Vincula los eventos con las funciones correspondientes
btn_obtener_datos.bind("<Enter>", on_enter)
btn_obtener_datos.bind("<Leave>", on_leave)

# Define las columnas del Treeview
columns = ('Empresa', 'NIS', 'Fecha Deposito', 'Fecha Corte', 'Importe', 'Tasa', 'Deposito semestre inicial', 'D_Ult_semestre', 'D_F')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Configura las columnas y los encabezados
for col in columns:
    tree.column(col, width=95)
    tree.heading(col, text=col)

# Estilo para el Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", fieldbackground=COLOR_FONDO, foreground=COLOR_TEXTO)
style.configure("Treeview.Heading", font=("Arial", 12), background=COLOR_BOTON, foreground=COLOR_TEXTO)
# Establece los colores de las filas alternas
style.configure("Treeview", background="#E8E8E8")  # Color de fondo predeterminado

# Configura el color de fondo de una fila cuando está seleccionada
style.map("Treeview", background=[('selected', COLOR_BOTON)])

# Añade un scrollbar al Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(expand=True, fill='both', padx=10, pady=5)

# Ejecutar el bucle principal de la GUI
root.mainloop()