from cryptography.fernet import Fernet

class CryptoUtils:
    @staticmethod
    def generate_key():
        return Fernet.generate_key()

    @staticmethod
    def encrypt_data(data, key):
        return Fernet(key).encrypt(data.encode())

    @staticmethod
    def decrypt_data(data, key):
        return Fernet(key).decrypt(data).decode()