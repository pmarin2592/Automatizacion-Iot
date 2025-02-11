from  database import get_db_connection
from models.lecturas_model import Lecturas
import pyodbc
from datetime import datetime

class LecturasService:
    @staticmethod
    def registro_lectura(tipoSensor, fechaHora):
        """
        Registra una nueva lectura en la base de datos.

        Parámetros:
        - tipoSensor (str): Tipo de sensor del cual se registra la lectura.
        - fechaHora (str): Fecha y hora de la lectura en formato adecuado.

        Retorna:
        - dict: Mensaje de éxito o error en caso de falla en la base de datos.
        """
        try:
            conn = get_db_connection() # Obtener conexión a la base de datos
            cursor = conn.cursor()

            try:
                # Ejecutar procedimiento almacenado para registrar la lectura
                cursor.execute("EXEC GenerarLecturasSensor_PR ?, ?",
                       (tipoSensor,fechaHora))
                conn.commit() # Confirmar la transacción
               
                return{"mensaje":"Registro de lectura exitoso"}
            
            except pyodbc.DatabaseError as db_err:
                conn.rollback()  # Deshacer cambios en caso de error en la BD
                return {"error": "Error en la base de datos", "detalle": str(db_err)}

            except Exception as e:
                return {"error": "Error desconocido", "detalle": str(e)}

                  
        
        except pyodbc.InterfaceError:
            return {"error": "No se pudo conectar a la base de datos"}

        except pyodbc.Error as db_conn_err:
            return {"error": "Error en la conexión con la base de datos", "detalle": str(db_conn_err)}

        finally:
            # Cerrar la conexión a la base de datos en el bloque `finally`
            if 'conn' in locals() and conn:
                conn.close()

        
    @staticmethod
    def obtener_lecturas_sensor(id):
        """
        Obtiene las lecturas de un sensor específico.

        Parámetros:
        - id (int): Identificador único del sensor.

        Retorna:
        - list[dict]: Lista de lecturas en formato de diccionario o mensaje de error.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                 # Ejecutar procedimiento almacenado para obtener las lecturas del sensor
                cursor.execute("EXEC ObtenerLecturaSensor_PR ? ",
                        (id))
                sensor = [Lecturas(row[0],row[1],row[2],row[3]).to_dict() for row in cursor.fetchall()]
                
                return sensor
            
            except pyodbc.DatabaseError as db_err:
                conn.rollback()  # Deshacer cambios en caso de error en la BD
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

    @staticmethod
    def obtener_lecturas_sensor_fechas(fec_inicio, fec_fin):
        """
        Obtiene las lecturas de todos los sensores en un rango de fechas.

        Parámetros:
        - fec_inicio (date): fecha de inicio 
        - fec_fin (date): fecha de fin 

        Retorna:
        - list[dict]: Lista de lecturas en formato de diccionario o mensaje de error.
        """
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                # Asegúrate de que fec_inicio y fec_fin sean de tipo datetime.date
                # Si fec_inicio o fec_fin son cadenas de texto con prefijos (ej. 'fecInicio=2025-01-01'),
                # eliminamos el prefijo y luego convertimos a tipo fecha
                if isinstance(fec_inicio, str):
                    fec_inicio = fec_inicio.split('=')[1]  # Eliminar el prefijo
                    fec_inicio = datetime.strptime(fec_inicio, "%Y-%m-%d").date()  # Convertir a tipo fecha
                if isinstance(fec_fin, str):
                    fec_fin = fec_fin.split('=')[1]  # Eliminar el prefijo
                    fec_fin = datetime.strptime(fec_fin, "%Y-%m-%d").date()  # Convertir a tipo fecha

                # Ejecutar procedimiento almacenado para obtener las lecturas del sensor
                cursor.execute("EXEC ObtenerLecturasFechas_PR ?, ?", (fec_inicio, fec_fin))
                sensor = [Lecturas(row[0], row[1], row[2], row[3]).to_dict() for row in cursor.fetchall()]
                
                return sensor
            
            except pyodbc.DatabaseError as db_err:
                conn.rollback()  # Deshacer cambios en caso de error en la BD
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
