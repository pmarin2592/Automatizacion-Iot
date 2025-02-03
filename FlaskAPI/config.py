from encryption import decrypt_message

class Config:
    DRIVER = '{ODBC Driver 18 for SQL Server}'
    SERVER = '20.119.72.230'
    DATABASE = 'IotBD'
    USERNAME = 'sa'
    PASSWORD_ENCRYPTED = 'gAAAAABnnqxaRvSt29kz5NXfS1SjnKHjxoFAFnsj4fs3uharbQY_cGQmZi202aav_-Ap6kJg-LkKTBHf850f7IOZKJZh1TGO6g=='  # Reemplaza con tu contraseña encriptada
   
    @classmethod
    def get_decrypted_password(cls):
        return decrypt_message(cls.PASSWORD_ENCRYPTED)
