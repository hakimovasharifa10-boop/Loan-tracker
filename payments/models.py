from django.db import models
from django.contrib.auth import get_user_model
from loans.models import Loan

User = get_user_model()

class Payment(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    loan  = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.loan.bank_name} - {self.amount} - {self.date}'

    class Meta:
        ordering = ['-date']
        