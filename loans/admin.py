from django.contrib import admin
from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        'bank_name',
        'user',
        'amount',
        'interest_rate',
        'monthly_payment',
        'end_date',
        'is_overdue',
        'show_status',
    )

    list_filter = ('bank_name', 'start_date')
    search_fields = ('bank_name', 'user__username', 'notes')
    date_hierarchy = 'start_date'

    def show_status(self, obj):
        status = obj.status_label

        if status == 'closed':
            return 'Closed'
        elif status == 'overdue':
            return 'Overdue'
        return 'Active'

    show_status.short_description = 'Status'
