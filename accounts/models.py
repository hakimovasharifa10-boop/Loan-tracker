from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class EmailConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_confirm')
    code = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.user.username} - {self.code}'
    
    
