import dash
from dash import dcc, html, Output, Input
import plotly.graph_objs as go
import requests
import time
import numpy as np
from datetime import datetime


# Configuración de la API y sensores
API_URL = "http://127.0.0.1:5000/lecturas/consulta/"
SENSORES = {
    "Temperatura": 1,
    "Consumo Eléctrico": 2,
    "Ocupación": 3,
    "Luz Ambiental": 4,
    "Humedad": 5
}

# Crear la app Dash
app = dash.Dash(__name__)

# Diseño del dashboard
app.layout = html.Div([
    html.H1("📊 Monitoreo de Sensores IoT"),
    
    # Contenedores para cada sensor
    *[
        html.Div([
            html.H3(sensor),
            dcc.Graph(id=f"graph-{sensor}"),
            html.Div(id=f"alert-{sensor}", style={"color": "red", "font-weight": "bold"})
        ])
        for sensor in SENSORES
    ],
    
    # Intervalo de actualización cada 3 minutos
    dcc.Interval(id="interval", interval=60 * 1000, n_intervals=0)
])

# Función para obtener datos de la API
def obtener_datos(sensor_id):
    try:
        response = requests.get(f"{API_URL}{sensor_id}")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                tiempos = [datetime.strptime(d["Fecha Hora"], "%a, %d %b %Y %H:%M:%S %Z") for d in data]
                valores = [float(d["Valor"]) for d in data]
                return tiempos, valores
        return [], []
    except requests.exceptions.RequestException:
        return [], []
    
# Función para detectar anomalías usando IQR
def detectar_anomalias(datos):
    if len(datos) < 5:
        return None

    Q1 = np.percentile(datos, 25)
    Q3 = np.percentile(datos, 75)
    IQR = Q3 - Q1

    limite_superior = Q3 + 1.5 * IQR
    valores_anomalos = [valor for valor in datos if valor > limite_superior]

    return valores_anomalos if valores_anomalos else None

# Crear callbacks dinámicos para cada sensor
@app.callback(
    [Output(f"graph-{sensor}", "figure") for sensor in SENSORES] +
    [Output(f"alert-{sensor}", "children") for sensor in SENSORES],
    Input("interval", "n_intervals")
)
def actualizar_graficos(n):
    figuras = []
    alertas = []
    
    for sensor, sensor_id in SENSORES.items():
        tiempos, valores = obtener_datos(sensor_id)
        
        if not valores:
            figuras.append(go.Figure())  # Si no hay datos, gráfico vacío
            alertas.append("⚠️ No hay datos disponibles.")
            continue

        # Detectar anomalías
        valores_anomalos = detectar_anomalias(valores)
        tiempos_anomalos = [tiempos[i] for i, v in enumerate(valores) if v in valores_anomalos] if valores_anomalos else []

        # Crear gráfico con fechas en el eje X
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=tiempos, y=valores, mode="lines+markers", name="Datos"))

        if valores_anomalos:
            fig.add_trace(go.Scatter(
                x=tiempos_anomalos, 
                y=valores_anomalos, 
                mode="markers", 
                marker=dict(color="red", size=10),
                name="Anomalías"
            ))
            alertas.append(html.Div([
                "⚠️ Anomalías detectadas:",
                html.Ul([html.Li(f"{t.strftime('%Y-%m-%d %H:%M:%S')} → {v:.2f}") for t, v in zip(tiempos_anomalos, valores_anomalos)], style={"color": "red"})
            ]))
        else:
            alertas.append("✅ Todo en orden.")

        fig.update_layout(
            xaxis_title="Tiempo",
            yaxis_title="Valor del Sensor",
            xaxis=dict(type="date"),  # Eje X como fechas reales
            title=f"Sensor: {sensor}"
        )

        figuras.append(fig)

    return figuras + alertas

# Ejecutar la app
if __name__ == "__main__":
    app.run_server(debug=True)
