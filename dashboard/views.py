from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from loans.models import Loan
from payments.models import Payment
import requests

def get_exchange_rates():
    try:
        response = requests.get(
            'https://api.exchangerate-api.com/v4/latest/TJS',
            timeout=5
        )
        data = response.json()
        return {
            'USD': round(data['rates']['USD'], 4),
            'RUB': round(data['rates']['RUB'], 2),
            'EUR': round(data['rates']['EUR'], 4),
        }
    except:
        return {'USD': 0.092, 'RUB': 8.5, 'EUR': 0.085}
    
@login_required
def dashboard_view(request):
    loans = Loan.objects.filter(user=request.user)
    payments = Payment.objects.filter(user=request.user)
    today = timezone.now().date()

    
    total_debt = sum(loan.remaining_amount() for loan in loans)
    total_paid = sum(p.amount for p in payments)
    active_loans = loans.count()
    
    overdue_loans = [loan for loan in loans if loan.end_date < today]

    
    upcoming_loans = sorted(
        [loan for loan in loans if loan.end_date >= today],
        key=lambda x: x.end_date
    )
    next_payment = upcoming_loans[0] if upcoming_loans else None


    recent_payments = payments[:5]

    
    rates = get_exchange_rates()
    
    
    return render(request, 'dashboard/dashboard.html', {
        'loans':           loans,
        'total_debt':      total_debt,
        'total_paid':      total_paid,
        'active_loans':    active_loans,
        'overdue_loans':   overdue_loans,
        'next_payment':    next_payment,
        'recent_payments': recent_payments,
        'rates':           rates,
        'today':           today,
    })

