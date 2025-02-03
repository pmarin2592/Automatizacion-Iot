import multiprocessing as mp
import requests
import time
import smtplib
import numpy as np
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración de la API y sensores
API_URL = "http://127.0.0.1:5000/lecturas/consulta/"
SENSORES = {
    "Temperatura": 1,
    "Consumo Eléctrico": 2,
    "Ocupación": 3,
    "Luz Ambiental": 4,
    "Humedad": 5
}


def detectar_anomalias_old(sensor, datos, umbral_factor=3):
    """Detecta anomalías usando el cálculo de Z-score."""
    if len(datos) < 5:  # Se necesita un mínimo de datos para el análisis
        return None
    
    media = np.mean(datos)
    desviacion = np.std(datos)

    if desviacion == 0:
        return None  # Evitar divisiones por cero

    ultimo_valor = datos[-1]
    z_score = (ultimo_valor - media) / desviacion

    if z_score > umbral_factor:
        return ultimo_valor, media + umbral_factor * desviacion

    return None

def obtener_datos(sensor_id):
    """Consulta la API y obtiene datos del sensor específico."""
    try:
        response = requests.get(f"{API_URL}{sensor_id}")
        if response.status_code == 200:
            data = response.json()
            # Si la respuesta es una lista, retornamos los datos directamente
            if isinstance(data, list):
                return data
            # Si la respuesta es un diccionario, intentamos obtener los valores
            return data.get("valores", [])
        else:
            print(f"Error en la API: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error obteniendo datos de la API: {e}")
        return []

def detectar_anomalias(sensor, datos, umbral_factor=1.5):
    """Detecta anomalías usando el rango intercuartilico (IQR)."""
    if len(datos) < 5:
        return None
    
    Q1 = np.percentile(datos, 25)  # Primer cuartil (Q1)
    Q3 = np.percentile(datos, 75)  # Tercer cuartil (Q3)
    IQR = Q3 - Q1  # Rango intercuartilico

    limite_inferior = Q1 - umbral_factor * IQR
    limite_superior = Q3 + umbral_factor * IQR

    print(f"{sensor}: Q1={Q1}, Q3={Q3}, IQR={IQR}, Límite inferior={limite_inferior}, Límite superior={limite_superior}")

    valores_anomalos = [valor for valor in datos if valor < limite_inferior or valor > limite_superior]

    if valores_anomalos:
        return valores_anomalos[0], limite_superior  # Devolver el primer valor anómalo encontrado

    return None

def monitorear_sensor(sensor, sensor_id, umbral_factor=1.2):
    """Monitorea un sensor en tiempo real, detectando anomalías y enviando alertas."""
    historial = []  # Lista para almacenar valores previos

    while True:
        print(f"Consultando datos para {sensor}...")
        datos = obtener_datos(sensor_id)
       
        if datos:
            # Extraer los valores numéricos de cada diccionario en `datos`
            valores = [float(dato["Valor"]) for dato in datos]  # Convertimos los valores a flotantes
            #print(f"{valores}")
            historial.extend(valores)
            historial = historial[-50:]  # Mantener solo las últimas 50 lecturas

            resultado = detectar_anomalias(sensor, historial, umbral_factor)
            if resultado:
                valor_anomalo, umbral = resultado
                print(f"⚠️ Anomalía detectada en {sensor}: {valor_anomalo} (umbral: {umbral})")              
            else:
                print(f"{sensor} dentro de valores normales.")
        
        time.sleep(180)  # Espera 3 minutos antes de la siguiente consulta

if __name__ == "__main__":
    procesos = []

    for sensor, sensor_id in SENSORES.items():
        p = mp.Process(target=monitorear_sensor, args=(sensor, sensor_id), name=f"Monitor-{sensor}")
        procesos.append(p)
        p.start()

    for p in procesos:
        p.join()
