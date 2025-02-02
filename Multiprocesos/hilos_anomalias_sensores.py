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

# Configuración del correo
EMAIL_SENDER = "304600713@cuc.cr"
EMAIL_PASSWORD = "Fullmetal2592$"
EMAIL_RECEIVER = "304600713@cuc.cr"
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

def enviar_alerta(sensor, valor, umbral):
    """Envía un correo si se detecta una anomalía en el sensor."""
    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = EMAIL_SENDER
        mensaje["To"] = EMAIL_RECEIVER
        mensaje["Subject"] = f"⚠️ Alerta de Consumo Anómalo en {sensor}"

        cuerpo = f"Se detectó un pico de consumo en el sensor {sensor}.\n"
        cuerpo += f"Valor detectado: {valor}\n"
        cuerpo += f"Umbral permitido: {umbral}\n"
        cuerpo += f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

        mensaje.attach(MIMEText(cuerpo, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, mensaje.as_string())
        server.quit()

        print(f"Correo de alerta enviado para {sensor}.")

    except Exception as e:
        print(f"Error enviando alerta: {e}")

def detectar_anomalias(sensor, datos, umbral_factor=3):
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

def monitorear_sensor(sensor, sensor_id, umbral_factor=3):
    """Monitorea un sensor en tiempo real, detectando anomalías y enviando alertas."""
    historial = []  # Lista para almacenar valores previos

    while True:
        print(f"Consultando datos para {sensor}...")
        datos = obtener_datos(sensor_id)

        if datos:
            # Extraer los valores numéricos de cada diccionario en `datos`
            valores = [float(dato["Valor"]) for dato in datos]  # Convertimos los valores a flotantes

            historial.extend(valores)
            historial = historial[-50:]  # Mantener solo las últimas 50 lecturas

            resultado = detectar_anomalias(sensor, historial, umbral_factor)
            if resultado:
                valor_anomalo, umbral = resultado
                print(f"⚠️ Anomalía detectada en {sensor}: {valor_anomalo} (umbral: {umbral})")
                enviar_alerta(sensor, valor_anomalo, umbral)
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
