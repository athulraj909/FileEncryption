from django.db import models
from .encryption import generate_key, encrypt_file,decrypt_file
import os
# Create your models here.

class User(models.Model):
    username=models.CharField(unique=True,max_length=200)
    email=models.CharField(unique=True,max_length=200)
    password=models.CharField(max_length=200)
    def __str__(self):
        return self.username
    




class EncryptedFile(models.Model):
    algorithm_choices = [
        ('hashes.SHA256', 'hashes.SHA256'),
        ('hashes.SHA384', 'hashes.SHA384'),
        ('hashes.SHA512', 'hashes.SHA512'),
        # Add more algorithms as needed
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField()
    password = models.CharField(max_length=100)
    algorith = models.CharField(max_length=20, choices=algorithm_choices)

    def save(self, *args, **kwargs):
        if not self.id:  # New instance being created
            super().save(*args, **kwargs)
            
            password_bytes = self.password.encode()
            salt = b'salt_'  # Change this to a proper salt value
            
            # Generate a key using the password and the chosen algorithm
            key = generate_key(password_bytes, self.algorith, salt)
            
            with open(self.file.path, 'rb') as file:
                file_content = file.read()
            
            # Encrypt the file content using the generated key
            encrypted_content = encrypt_file(file_content, key)
            
            # Save the encrypted content back to the file
            with open(self.file.path, 'wb') as file:
                file.write(encrypted_content)
        
        super().save(*args, **kwargs)


    def __str__(self):
        return self.file.name
