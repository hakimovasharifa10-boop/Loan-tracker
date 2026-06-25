from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Loan(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    bank_name      = models.CharField(max_length=200)
    logo           = models.ImageField(upload_to='bank_logos/', null=True, blank=True)
    amount         = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate  = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_payment= models.DecimalField(max_digits=12, decimal_places=2)
    start_date     = models.DateField()
    end_date       = models.DateField()
    notes          = models.TextField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)