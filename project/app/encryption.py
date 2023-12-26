# encryption.py

from cryptography.fernet import Fernet

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from cryptography.fernet import Fernet
import base64
import hashlib


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



def derive_key_from_password(password, algorithm):
    if password is None:
        raise ValueError("Password is required")
    
    # Use a salt value for key derivation
    salt = b'some_salt_value'  # Replace this with a proper salt value
    
    if algorithm == 'hashes.SHA256':
        kdf = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    elif algorithm == 'hashes.SHA384':
        kdf = hashlib.pbkdf2_hmac('sha384', password.encode('utf-8'), salt, 100000)
    elif algorithm == 'hashes.SHA512':
        kdf = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    else:
        raise ValueError("Invalid algorithm")

    key = base64.urlsafe_b64encode(kdf)
    return key

