from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('loan', 'user', 'amount', 'date', 'notes')
    list_filter   = ('date', 'loan__bank_name')
    search_fields = ('loan__bank_name', 'user__username', 'notes')
    date_hierarchy = 'date'
    ordering = ('-date',)
