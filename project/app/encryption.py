# encryption.py

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from cryptography.fernet import Fernet
import base64


def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations as needed
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key





def encrypt_file(file_content, key):
    f = Fernet(key)
    encrypted_content = f.encrypt(file_content)
    return encrypted_content

def decrypt_file(encrypted_content, key):
    f = Fernet(key)
    decrypted_content = f.decrypt(encrypted_content)
    return decrypted_content
