# encryption.py

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from cryptography.fernet import Fernet
import base64


def generate_key(password, algorith, salt):
    # Convert algorithm string to the actual algorithm object
    if algorith == 'hashes.SHA256':
        algo = hashes.SHA256()
    elif algorith == 'hashes.SHA384':
        algo = hashes.SHA384()
    elif algorith == 'hashes.SHA512':
        algo = hashes.SHA512()
    else:
        # Handle the case when an invalid algorithm is provided
        raise ValueError("Invalid algorithm")
    
    kdf = PBKDF2HMAC(
        algorithm=algo,
        length=32,
        salt=salt,
        iterations=100000,
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
