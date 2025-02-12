import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, PowerTransformer
import plotly.graph_objects as go
import plotly.express as px

# Configuración de la API y sensores
api_url = "http://20.115.90.45:80/lecturas/consultaSensores/"

# Configuración de la interfaz
st.set_page_config(layout="wide")
st.title("📊 Análisis de Sensores desde API")

# Entrada de API y rango de fechas
col1, col2 = st.columns(2)
start_date = col1.date_input("📅 Fecha de inicio")
end_date = col2.date_input("📅 Fecha de fin")


# --- 📌 FUNCIONES --- 
def obtener_datos(api_url, start_date, end_date):
    """Obtiene datos desde la API según el rango de fechas."""
    try:
        url = f"{api_url}/fecInicio={start_date.strftime('%Y-%m-%d')}/fecFin={end_date.strftime('%Y-%m-%d')}"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()

        # Asegurarse de que data es una lista de diccionarios antes de crear el DataFrame
        if isinstance(data, dict):  # Si la API devuelve un solo objeto en lugar de una lista
            data = [data]  # Convertirlo en una lista de un solo elemento

        print(data)
        return pd.DataFrame(data) if isinstance(data, list) else pd.DataFrame()
    
    except Exception as e:
        st.error(f"❌ Error al obtener datos: {e}")
        return pd.DataFrame()


def procesar_datos(df):
    """Transforma los datos: normalización y corrección de distribución."""
    
    # 🔍 Mostrar nombres de columnas antes de renombrar
    print("Columnas originales del DataFrame:", df.columns.tolist())

    # 🔹 Eliminar espacios invisibles y caracteres ocultos en los nombres de columnas
    df.columns = df.columns.str.strip().str.replace("\xa0", "").str.replace("\u200b", "")

    # 🔍 Mostrar nombres de columnas después de limpiar
    print("Columnas después de limpiar:", df.columns.tolist())

    # Renombrar la columna para evitar errores de acceso
    df.rename(columns={"Fecha Hora": "Fecha_Hora", "Id sensor": "ID Sensor"}, inplace=True)

    # 🔍 Verificar nombres de columnas después del renombrado
    print("Columnas después del renombrado:", df.columns.tolist())

    # ✅ Verificar si la columna "Fecha_Hora" existe
    if "Fecha_Hora" not in df.columns:
        raise KeyError("❌ La columna 'Fecha_Hora' no fue encontrada después del renombrado.")

    # Intentar convertir la columna a datetime
    df["Fecha_Hora"] = pd.to_datetime(df["Fecha_Hora"])

    # Asegurar que la columna 'Valor' sea numérica
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")  # Los valores no numéricos se convierten en NaN

    # Eliminar filas con valores NaN en 'Valor' (opcional)
    df.dropna(subset=["Valor"], inplace=True)

    # Eliminar duplicados o agrupar los datos (por ejemplo, tomando el promedio de los valores)
    df = df.groupby(["Fecha_Hora", "ID Sensor"], as_index=False)["Valor"].mean()

    # Pivotear los datos para organizar por sensor
    df_pivot = df.pivot(index="Fecha_Hora", columns="ID Sensor", values="Valor")

    # Renombrar sensores
    sensor_mapping = {1: "temperatura", 2: "consumo_electrico", 3: "ocupacion", 4: "luz_ambiental", 5: "humedad"}
    df_pivot.rename(columns=sensor_mapping, inplace=True)
    df_pivot.reset_index(inplace=True)

    # Normalización y transformación
    sensor_cols = [col for col in df_pivot.columns if col != "Fecha_Hora"]
    scaler = MinMaxScaler()
    transformer = PowerTransformer(method="yeo-johnson")

    for col in sensor_cols:
        df_pivot[col] = df_pivot[col].astype(float)  # Asegurar que sean numéricos
        df_pivot[col].fillna(df_pivot[col].median(), inplace=True)
        df_pivot[col + "_norm"] = scaler.fit_transform(df_pivot[[col]])
        df_pivot[col + "_transf"] = transformer.fit_transform(df_pivot[[col]])

    return df_pivot, sensor_cols



def graficar_distribuciones(df, sensor_cols):
    """Genera histogramas y boxplots para cada sensor con mejor legibilidad y formato mejorado."""
    for col in sensor_cols:
        st.markdown(f"### 🔍 Análisis de `{col}`")

        fig, axes = plt.subplots(2, 3, figsize=(20, 10), gridspec_kw={'hspace': 0.4})  # Ajuste del espacio
        
        # Histogramas
        sns.histplot(df[col], ax=axes[0, 0], kde=True, color="skyblue", bins=50)
        axes[0, 0].set_title(f"{col} - Original", fontsize=14)
        axes[0, 0].set_xlabel(col)
        axes[0, 0].set_ylabel("Count")

        sns.histplot(df[col + "_norm"], ax=axes[0, 1], kde=True, color="orange", bins=50)
        axes[0, 1].set_title(f"{col} - Normalizado", fontsize=14)
        axes[0, 1].set_xlabel(f"{col}_norm")
        axes[0, 1].set_ylabel("Count")

        sns.histplot(df[col + "_transf"], ax=axes[0, 2], kde=True, color="green", bins=50)
        axes[0, 2].set_title(f"{col} - Transformado", fontsize=14)
        axes[0, 2].set_xlabel(f"{col}_transf")
        axes[0, 2].set_ylabel("Count")

        # Boxplots
        sns.boxplot(y=df[col], ax=axes[1, 0], color="skyblue", width=0.5)
        axes[1, 0].set_title(f"{col} - Boxplot Original", fontsize=14)

        sns.boxplot(y=df[col + "_norm"], ax=axes[1, 1], color="orange", width=0.5)
        axes[1, 1].set_title(f"{col} - Boxplot Normalizado", fontsize=14)

        sns.boxplot(y=df[col + "_transf"], ax=axes[1, 2], color="green", width=0.5)
        axes[1, 2].set_title(f"{col} - Boxplot Transformado", fontsize=14)

        plt.tight_layout()  # Ajustar automáticamente los espacios

        st.pyplot(fig)  # Mostrar en Streamlit

def graficar_tendencias(df, sensor_cols):
    """Genera gráfico de líneas interactivo con Plotly."""
    st.subheader("📈 Tendencia Temporal de los Sensores")

    fig = px.line(df, x="Fecha_Hora", y=[col + "_norm" for col in sensor_cols], 
                  labels={"value": "Valor Normalizado", "variable": "Sensor"}, 
                  title="Evolución de Sensores Normalizados")

    fig.update_layout(
        hovermode="x unified",  # Mostrar todos los valores al pasar el cursor
        xaxis_title="Fecha",
        yaxis_title="Valor Normalizado"
    )

    st.plotly_chart(fig, use_container_width=True)



def graficar_correlacion(df, sensor_cols):
    """Muestra un heatmap de correlación entre los sensores."""
    st.subheader("📊 Correlación entre Sensores")
    fig, ax = plt.subplots(figsize=(10, 6))
    corr_matrix = df[sensor_cols].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
    ax.set_title("Mapa de Correlaciones entre Sensores")
    st.pyplot(fig)


def descargar_csv(df):
    """Permite descargar el CSV con los datos procesados."""
    csv_filename = "data_transformed.csv"
    df.to_csv(csv_filename, index=False)
    st.download_button(label="📥 Descargar CSV", data=open(csv_filename, "rb").read(),
                       file_name=csv_filename, mime="text/csv")


# --- 🚀 EJECUCIÓN PRINCIPAL ---
if st.button("🚀 Obtener Datos y Analizar"):
    df = obtener_datos(api_url, start_date, end_date)
    
    if not df.empty:
        df_pivot, sensor_cols = procesar_datos(df)
        
        # Mostrar tabla de datos transformados
        st.write("📋 **Vista previa de los datos transformados:**")
        st.dataframe(df_pivot.head())

        # Generar visualizaciones
        graficar_distribuciones(df_pivot, sensor_cols)
        graficar_tendencias(df_pivot, sensor_cols)
        graficar_correlacion(df_pivot, sensor_cols)

        # Botón de descarga
        descargar_csv(df_pivot)
