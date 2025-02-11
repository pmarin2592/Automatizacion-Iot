import pyodbc
import multiprocessing

# Define los parámetros de conexión
server = r'DESKTOP-U4E3J7V\SQLEXPRESS'
database = 'prueba'  # Nombre de tu base de datos
driver = '{ODBC Driver 17 for SQL Server}'

# Establece la conexión usando la autenticación de Windows
conn = pyodbc.connect(
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'Trusted_Connection=yes;'
)

# Crea un cursor
cursor = conn.cursor()

# Ejecuta una consulta SQL para extraer datos
query = "SELECT * FROM Sensores"
cursor.execute(query)


# Recupera los resultados
resultados = cursor.fetchall()



# Cierra la conexión
conn.close()

# Función para mostrar temperaturas mayores a 18
def mostrar_mayor_18(temp):
    if temp > 18:
        print(f"La temperatura {temp} es mayor a 18 grados")

if __name__ == '__main__':
    # Crear una lista de procesos
    procesos = []
    for fila in resultados:
        # Convertir la temperatura a entero antes de pasarla a la función
        temp = int(fila.temperatura)
        p = multiprocessing.Process(target=mostrar_mayor_18, args=(temp,))
        procesos.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in procesos:
        p.join()
    print(resultados)
    print('Todos los procesos han terminado.')

