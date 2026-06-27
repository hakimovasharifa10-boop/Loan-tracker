from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Goal(models.Model):
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('completed', 'Completed'),
        ('failed',    'Failed'),
    ]

    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title          = models.CharField(max_length=200)
    description    = models.TextField(blank=True)
    target_amount  = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date    = models.DateField()
    icon           = models.CharField(max_length=10, default='🎯')
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def progress_percent(self):
        if self.target_amount == 0:
            return 0
        return min(int((self.current_amount / self.target_amount) * 100), 100)

    def remaining_amount(self):
        return self.target_amount - self.current_amount

    def days_left(self):
        today = timezone.now().date()
        delta = (self.target_date - today).days
        return max(delta, 0)

    def monthly_needed(self):
        days = self.days_left()
        if days <= 0:
            return self.remaining_amount()
        months = max(days / 30, 1)
        return round(float(self.remaining_amount()) / months, 2)

    def is_overdue(self):
        return self.target_date < timezone.now().date() and self.status == 'active'
