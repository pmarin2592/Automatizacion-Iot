import pyodbc
from config import Config

def get_db_connection():
    """
    Establece y retorna una conexión a la base de datos SQL Server.

    Retorna:
        pyodbc.Connection: Objeto de conexión a la base de datos.

    Excepciones:
        Lanza un error si la conexión falla.
    """
    conn = pyodbc.connect(
        f"DRIVER={Config.DRIVER};"
        f"SERVER={Config.SERVER};"
        f"DATABASE={Config.DATABASE};"
        f"UID={Config.USERNAME};"
        f"PWD={Config.get_decrypted_password()};"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
    )
    return conn
