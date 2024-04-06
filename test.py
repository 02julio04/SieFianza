import tkinter as tk
from tkinter import ttk
import pyodbc
import DB
from Sie import SieFianza

# Replace 'your_server' and 'your_database' with the actual server and database names
server = 'PEDROJULIO'
database = 'Db_SIE'

# Construct connection string for Windows Authentication
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes'
db = DB.Database(conn_str)  # Create a new instance

# Definir la función que se llamará cuando se presione el botón 'Obtener Datos'
def on_obtener_datos():
    empresa_input = empresa_entry.get().upper()  # Suponemos que tienes una Entry para ingresar el nombre de la empresa
    if empresa_input in ["EDEESTE", "EDESUR", "EDENORTE"]:
        try:
            # Obtiene los datos llamando a la función SieFianza
            datos = SieFianza(empresa_input)
            # Actualiza la GUI con los datos
            update_gui_with_data(datos)
        except Exception as e:
            print(f"Error al obtener datos: {e}")
    else:
        print("Empresa no reconocida. Por favor, ingresa una empresa válida.")

# Función que actualiza la GUI con los datos obtenidos
def update_gui_with_data(datos):
    tree.delete(*tree.get_children())
    for dato in datos:
        tree.insert("", "end", values=dato)

# Crea la ventana principal
root = tk.Tk()
root.title("Calculadora de Depósitos")

# Configura las columnas del Treeview
columns = ('Empresa', 'NIS', 'Fecha Deposito', 'Fecha Corte', 'Importe')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Define los encabezados
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

# Añade un scrollbar al Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.pack(side='right', fill='y')
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(expand=True, fill='both')

# Crea el área de entrada para el nombre de la empresa
empresa_label = tk.Label(root, text="Empresa:")
empresa_label.pack(side='top', pady=5)
empresa_entry = tk.Entry(root)
empresa_entry.pack(side='top', pady=5)

# Botón para obtener los datos
btn_obtener_datos = tk.Button(root, text='Obtener Datos', command=on_obtener_datos)
btn_obtener_datos.pack(side='top', pady=10)

# Inicia el loop principal de la GUI
root.mainloop()