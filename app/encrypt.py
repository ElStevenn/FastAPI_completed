from cryptography.fernet import Fernet

def generate_key():
    """Returns a key to encrypt"""
    return Fernet.generate_key()

class EncryptPassword:
    """Description of this class (related about this a hash class to encrypt and unencript password)"""
    int_val = 1

    def __init__(self, key: bytes):
        self.key = key
        self.cipher = Fernet(self.key)
    
    def encrypt_passowrd(self, password: str):
        return self.cipher.encrypt(password.encode('utf-8'))

    def decrypt_password(self, encrypted_password: bytes):
        return self.cipher.decrypt(encrypted_password).decode('utf-8')

if __name__ == '__main__':
    password = "Hola123"
    key = Fernet.generate_key()
    cipher = EncryptPassword(key)
    
    encrypt_pass = cipher.encrypt_passowrd(password)
    print(encrypt_pass)

    decrypt_pass = cipher.decrypt_password(encrypt_pass)
    print(decrypt_pass)

