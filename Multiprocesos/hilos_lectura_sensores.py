import multiprocessing as mp
import requests
import time
import random
from datetime import datetime

# -------------------------------
# 📌 CONFIGURACIÓN DEL SISTEMA DE SENSORES
# -------------------------------
# URL de la API para registrar datos de los sensores
API_URL = "http://127.0.0.1:5000/lecturas/registro"

# Mapeo de sensores a sus identificadores
SENSORES = {
    "Temperatura": 1,
    "Consumo Eléctrico": 2,
    "Ocupación": 3,
    "Luz Ambiental": 4,
    "Humedad": 5
}
# -------------------------------
# 🔄 GENERACIÓN DE DATOS DE SENSORES
# -------------------------------
def generar_datos(sensor, conn):
    """Genera datos para un sensor y los envía a través de un Pipe."""
    while True:
        fecha = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        conn.send((sensor, fecha))
        #intervalo = random.uniform(300, 900)  # Entre 5 y 15 minutos
        intervalo = random.uniform(60, 180)  # Entre 1 y 3 minutos
        print(f"{sensor}: Dato generado a las {fecha}, siguiente en {intervalo / 60:.2f} minutos")
        time.sleep(intervalo)
# -------------------------------
# 🚀 ENVÍO DE DATOS A LA API
# -------------------------------
def enviar_datos(conns):
    """Recibe datos del Pipe de todos los sensores y los envía a la API."""
    while True:
        for conn in conns:
            if conn.poll():  # Verifica si hay datos disponibles en el pipe
                sensor, fecha = conn.recv()
                payload = {"tipoSensor": sensor, "fechaHora": fecha}
                try:
                    response = requests.post(API_URL, json=payload)
                    print(f"[Hilo {mp.current_process().name}] Enviado: {payload} - Estado: {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"[Hilo {mp.current_process().name}] Error en la conexión: {e}")
# -------------------------------
# 🔄 CREACIÓN Y EJECUCIÓN DE PROCESOS
# -------------------------------
if __name__ == "__main__":
    procesos = []
    parent_conns = []
    
    # Crear procesos para generar datos
    for sensor in SENSORES.keys():
        parent_conn, child_conn = mp.Pipe()
        parent_conns.append(parent_conn)
        p = mp.Process(target=generar_datos, args=(sensor, child_conn), name=f"Generador-{sensor}")
        procesos.append(p)
        p.start()
    
    # Crear proceso para enviar datos desde todos los sensores
    p_envio = mp.Process(target=enviar_datos, args=(parent_conns,), name="Envío-Datos")
    procesos.append(p_envio)
    p_envio.start()
    
    # Monitorear procesos activos
    while True:
        print("Procesos activos:")
        for p in procesos:
            print(f"{p.name}: {'Activo' if p.is_alive() else 'Finalizado'}")
        time.sleep(60)  # Actualizar cada minuto
