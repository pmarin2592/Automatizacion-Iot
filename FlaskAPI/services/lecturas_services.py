from  database import get_db_connection
from models.lecturas_model import Lecturas
import pyodbc

class LecturasService:
    @staticmethod
    def registro_lectura(tipoSensor, fechaHora):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("EXEC GenerarLecturasSensor_PR ?, ?",
                       (tipoSensor,fechaHora))
                conn.commit()
               
                return{"mensaje":"Registro de lectura exitoso"}
            
            except pyodbc.DatabaseError as db_err:
                conn.rollback()  # Deshacer cambios en caso de error
                return {"error": "Error en la base de datos", "detalle": str(db_err)}

            except Exception as e:
                return {"error": "Error desconocido", "detalle": str(e)}

                  
        
        except pyodbc.InterfaceError:
            return {"error": "No se pudo conectar a la base de datos"}

        except pyodbc.Error as db_conn_err:
            return {"error": "Error en la conexión con la base de datos", "detalle": str(db_conn_err)}

        finally:
            if 'conn' in locals() and conn:
                conn.close()  # Cerrar la conexión en el bloque `finally`

        
