from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    bank_name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='bank_logos/', null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_payment= models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.bank_name} - {self.amount}'

    def paid_amount(self):
        return sum(p.amount for p in self.payments.all())

    def remaining_amount(self):
        return self.amount - self.paid_amount()

    def progress_percent(self):
        if self.amount == 0:
            return 0
        return round((self.paid_amount() / self.amount) * 100)
    
    def is_overdue(self):
        return self.end_date < timezone.now().date()

    class Meta:
        ordering = ['-created_at']