import pyodbc
from config import Config

def get_db_connection():
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
