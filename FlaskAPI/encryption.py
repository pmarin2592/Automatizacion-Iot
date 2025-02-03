# encryption.py
from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("secret.key", "rb").read()

def encrypt_message(message):
    key = load_key()
    return Fernet(key).encrypt(message.encode()).decode()

def decrypt_message(encrypted_message):
    key = load_key()
    return Fernet(key).decrypt(encrypted_message.encode()).decode()

if __name__ == "__main__":
    generate_key()  # Ejecutar solo una vez para generar la clave
    print(encrypt_message("Progra2025$"))
    print("Clave generada. Ahora encripta tus credenciales con encrypt_message().")
