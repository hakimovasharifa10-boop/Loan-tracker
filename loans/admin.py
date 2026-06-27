from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display  = ('bank_name', 'user', 'amount', 'interest_rate', 'monthly_payment', 'end_date', 'is_overdue')
    list_filter   = ('bank_name', 'start_date')
    search_fields = ('bank_name', 'user__username', 'notes')
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('User & Bank', {
            'fields': ('user', 'bank_name', 'logo')
        }),
        ('Loan Details', {
            'fields': ('amount', 'interest_rate', 'monthly_payment')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Extra', {
            'fields': ('notes',)
        }),
    )
