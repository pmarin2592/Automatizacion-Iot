import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# 📌 Configuración de la API
api_url = "http://127.0.0.1:5000/lecturas/consultaSensores/"

# 📊 Diccionario de Sensores: Relaciona el ID con el nombre del sensor
sensores = {
    1: "Temperatura",
    2: "Consumo Eléctrico",
    3: "Ocupación",
    4: "Luz Ambiental",
    5: "Humedad"
}

# 📌 Configuración de la interfaz en Streamlit
st.set_page_config(layout="wide")  # Pantalla ancha para mejor visualización
st.title("📊 Análisis de Patrones Temporales en Sensores")

# 📅 Entrada de rango de fechas
col1, col2 = st.columns(2)
start_date = col1.date_input("📅 Fecha de inicio")  # Selección de fecha inicial
end_date = col2.date_input("📅 Fecha de fin")  # Selección de fecha final


# 🔍 Función para obtener los datos desde la API
@st.cache_data  # Se almacena en caché para evitar múltiples solicitudes innecesarias
def obtener_datos(api_url, start_date, end_date):
    """Consulta los datos desde la API y los convierte en un DataFrame de Pandas."""
    try:
        url = f"{api_url}/fecInicio={start_date.strftime('%Y-%m-%d')}/fecFin={end_date.strftime('%Y-%m-%d')}"
        response = requests.get(url)
        response.raise_for_status()  # Lanza error si la respuesta es incorrecta (404, 500, etc.)
        data = response.json()  # Convierte la respuesta JSON en un diccionario
        if isinstance(data, dict):  
            data = [data]  # Convierte en lista si la API devuelve un solo objeto
        return pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error al obtener datos: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error


# 🔍 Función para procesar los datos
def procesar_datos(df):
    """Limpia y procesa los datos de sensores."""
    # 🔹 Limpieza de nombres de columnas (eliminación de caracteres invisibles)
    df.columns = df.columns.str.strip().str.replace("\xa0", "").str.replace("\u200b", "")

    # 🔹 Renombrar columnas clave para evitar errores
    df.rename(columns={"Fecha Hora": "Fecha_Hora", "Id sensor": "ID Sensor"}, inplace=True)

    # 🔹 Convertir columna de fecha y hora a formato datetime
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])

    # 🔹 Convertir la columna 'Valor' a formato numérico
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    # 🔹 Eliminar filas con valores nulos en 'Valor'
    df.dropna(subset=["Valor"], inplace=True)

    # 🔹 Agrupar los datos por 'Fecha_Hora' y 'ID Sensor' tomando el promedio
    df = df.groupby(["Fecha_Hora", "ID Sensor"], as_index=False)["Valor"].mean()

    return df


# 📊 Función para generar gráficos de patrones diarios, semanales y mensuales
def graficar_patrones_temporales(df_sensor, sensor_nombre):
    """Genera gráficos de análisis de patrones diarios, semanales y mensuales para cada sensor."""
    
    # 📌 Extraer características de la fecha
    df_sensor["Hora"] = df_sensor["Fecha_Hora"].dt.hour  # Hora del día
    df_sensor["Día_Semana"] = df_sensor["Fecha_Hora"].dt.day_name()  # Día de la semana
    df_sensor["Mes"] = df_sensor["Fecha_Hora"].dt.month_name()  # Mes del año

    # 📌 Crear una figura con 3 gráficos en una sola fila
    fig, axes = plt.subplots(1, 3, figsize=(20, 5))

    # 📅 Gráfico de Patrón Diario: Promedio de valores por hora
    sns.lineplot(data=df_sensor.groupby("Hora")["Valor"].mean(), marker="o", ax=axes[0], color="blue")
    axes[0].set_title(f"📅 Patrón Diario - {sensor_nombre}")
    axes[0].set_xlabel("Hora del día")
    axes[0].set_ylabel("Valor promedio")
    axes[0].grid()

    # 📆 Gráfico de Distribución por Día de la Semana
    sns.boxplot(x=df_sensor["Día_Semana"], y=df_sensor["Valor"], ax=axes[1], palette="Set2")
    axes[1].set_title(f"📆 Distribución por Día de la Semana - {sensor_nombre}")
    axes[1].set_xlabel("Día de la Semana")
    axes[1].set_ylabel("Valor")
    axes[1].grid()

    # 📊 Gráfico de Distribución por Mes
    sns.boxplot(x=df_sensor["Mes"], y=df_sensor["Valor"], ax=axes[2], palette="coolwarm")
    axes[2].set_title(f"📊 Distribución por Mes - {sensor_nombre}")
    axes[2].set_xlabel("Mes")
    axes[2].set_ylabel("Valor")
    axes[2].grid()

    plt.xticks(rotation=45)  # Rotar etiquetas del eje X para mejor lectura
    plt.tight_layout()  # Ajustar espacio entre gráficos
    
    st.pyplot(fig)  # Mostrar el gráfico en la interfaz de Streamlit


# 🚀 Ejecución Principal: Botón para iniciar el análisis
if st.button("🔄 Analizar Patrones"):
    df = procesar_datos(obtener_datos(api_url, start_date, end_date))  # Obtener y procesar datos

    if not df.empty:
        st.subheader("📊 Visualización de Patrones Temporales por Sensor")

        # 🔍 Analizar cada sensor por separado
        for sensor_id, sensor_nombre in sensores.items():
            df_sensor = df[df["ID Sensor"] == sensor_id]  # Filtrar datos por sensor específico
            if not df_sensor.empty:
                st.markdown(f"### 📡 {sensor_nombre}")  # Título del sensor
                graficar_patrones_temporales(df_sensor, sensor_nombre)  # Generar gráficos
            else:
                st.warning(f"⚠ No hay datos para {sensor_nombre}.")  # Advertencia si no hay datos
    else:
        st.warning("⚠ No hay datos disponibles para el rango de fechas seleccionado.")  # Advertencia global si no hay datos
