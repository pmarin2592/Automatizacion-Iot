from database import get_db_connection
from models.sensores_model import Sensores

class SensoresService:
    @staticmethod
    def get_all_sensores():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ID_Sensor ,Tipo ,Ubicacion ,Fecha_Instalacion ,Estado FROM Sensores")
        sensores = [Sensores(row[0],row[1],row[2], row[3], row[4]).to_dict() for row in cursor.fetchall()]
        conn.close()
        return sensores