from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username


class EmailConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_confirm')
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.user.username} - {self.code}'
    
    
