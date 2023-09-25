from cryptography.fernet import Fernet
import os, json



def generate_key():
    """Returns a key to encrypt"""
    key = Fernet.generate_key()
    key_file_path = os.path.join(os.getcwd(), "keys", "private_key.json")
    os.makedirs(os.path.dirname(key_file_path), exist_ok=True)

    with open(key_file_path, "wb") as f:
        f.write(key)



class EncryptPassword:
    """Description of this class (related about this a hash class to encrypt and unencript password)"""
    int_val = 1
    key_file_path = os.path.join(os.getcwd(), "keys", "private_key.json")

    def __init__(self, key: bytes):
        self.key = key
        self.cipher = Fernet(self.key)
    
    def encrypt_passowrd(self, password: str):
        return self.cipher.encrypt(password.encode('utf-8'))

    def decrypt_password(self, encrypted_password: bytes):
        return self.cipher.decrypt(encrypted_password).decode('utf-8')

    @classmethod
    def read_key(cls):
        with open(cls.key_file_path, "rb") as f:
            key = f.read()

        return key



if __name__ == '__main__':  
    My_Password = "Pau's Lol!"

    Key = EncryptPassword.read_key()
    Encrypter = EncryptPassword(Key)

    with open(os.getcwd() + "/keys/hashed_password.txt", "rb") as f:
        ecrp_pass = f.read()

    Decrypt_password = Encrypter.decrypt_password(ecrp_pass)
    print(Decrypt_password)



"""    
   

    Password_key = Encrypter.encrypt_passowrd(My_Password)

    with open(os.getcwd() + "/keys/hashed_password.txt", "wb") as f:
        f.write(Password_key)"""


    
    
