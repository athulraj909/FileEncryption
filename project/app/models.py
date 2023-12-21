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
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key relationship
    file = models.FileField()
    password = models.CharField(max_length=100)
    

    def save(self, *args, **kwargs):
        if not self.id:  # New instance being created
            super().save(*args, **kwargs)  # Save the model to ensure the file is saved
            
            # Get or generate the password and salt values
            password_bytes = self.password.encode()  # Convert password to bytes
            salt = b'salt_'  # Your own salt value
            
            # Generate a key using the password and salt
            key = generate_key(password_bytes, salt)
            
            # Read the file content from the uploaded file
            with open(self.file.path, 'rb') as file:
                file_content = file.read()
            
            # Encrypt the file content before saving
            encrypted_content = encrypt_file(file_content, key)
            
            # Overwrite the file content with the encrypted content
            with open(self.file.path, 'wb') as file:
                file.write(encrypted_content)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.file.name
