from database import get_db_connection
from models.sensores_model import Sensores

class SensoresService:
    @staticmethod
    def get_all_sensores():
        """
        Obtiene la lista de todos los sensores registrados en la base de datos.

        Retorna:
        - list[dict]: Lista de sensores con sus detalles en formato de diccionario.
        """
        conn = get_db_connection()# Obtener conexión a la base de datos
        cursor = conn.cursor()
         # Consultar todos los sensores de la base de datos
        cursor.execute("SELECT ID_Sensor ,Tipo ,Ubicacion ,Fecha_Instalacion ,Estado FROM Sensores")
        sensores = [Sensores(row[0],row[1],row[2], row[3], row[4]).to_dict() for row in cursor.fetchall()]
        conn.close()  # Cerrar la conexión
        return sensores