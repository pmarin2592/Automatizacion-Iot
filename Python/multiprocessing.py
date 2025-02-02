import pyodbc
import multiprocessing

# Define los parámetros de conexión
server = '20.119.72.230'
database = 'IotBD'  # Nombre de tu base de datos
driver = '{ODBC Driver 17 for SQL Server}'
username = 'sa'  # Reemplaza con tu nombre de usuario
password = 'Progra2025$' 

# Establece la conexión usando la autenticación de Windows
conn = pyodbc.connect(
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
)

# Crea un cursor
cursor = conn.cursor()

# Ejecuta una consulta SQL para extraer datos
query = "SELECT * FROM Lecturas_Sensores"
cursor.execute(query)

# Recupera los resultados
resultados = cursor.fetchall()

# Cierra la conexión
conn.close()

# Función para mostrar temperaturas mayores a 30
def mostrar_mayor_30(temp):
    if temp > 30:
        print(f"La temperatura {temp} es mayor a 30 grados")

if __name__ == '__main__':
    # Crear una lista de procesos
    procesos = []
    for fila in resultados:
        # Asegúrate de usar el nombre del campo correcto
        temp = int(fila.Valor)
        p = multiprocessing.Process(target=mostrar_mayor_30, args=(temp,))
        procesos.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()

    print('Todos los procesos han terminado.')
