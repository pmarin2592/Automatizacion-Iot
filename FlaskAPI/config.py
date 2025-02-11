from encryption import decrypt_message
# -------------------------------
# 🔒 CONFIGURACIÓN DE BASE DE DATOS
# -------------------------------
class Config:
    """
    Clase de configuración para la conexión a la base de datos SQL Server.
    Contiene los parámetros necesarios para la conexión, incluyendo el 
    método para desencriptar la contraseña almacenada de forma segura.
    """
    DRIVER = '{ODBC Driver 18 for SQL Server}'
    SERVER = '20.119.72.230'
    DATABASE = 'IotBD'
    USERNAME = 'sa'
    PASSWORD_ENCRYPTED = 'gAAAAABnnqxaRvSt29kz5NXfS1SjnKHjxoFAFnsj4fs3uharbQY_cGQmZi202aav_-Ap6kJg-LkKTBHf850f7IOZKJZh1TGO6g=='  # Reemplaza con tu contraseña encriptada
   
    @classmethod
    def get_decrypted_password(cls):
        """
        Método para obtener la contraseña desencriptada.
        Utiliza la función `decrypt_message` del módulo `encryption`.
        """
        return decrypt_message(cls.PASSWORD_ENCRYPTED)
