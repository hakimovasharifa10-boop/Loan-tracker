from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from loans.models import Loan
from payments.models import Payment
from datetime import timedelta
import requests
import json


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
    loans    = Loan.objects.filter(user=request.user)
    payments = Payment.objects.filter(user=request.user)
    today    = timezone.now().date()

    # Статистика
    total_debt    = sum(loan.remaining_amount() for loan in loans)
    total_paid    = sum(p.amount for p in payments)
    active_loans  = loans.count()

    # Просроченные кредиты
    overdue_loans = [loan for loan in loans if loan.end_date < today]

    # Ближайший платёж
    upcoming_loans = sorted(
        [loan for loan in loans if loan.end_date >= today],
        key=lambda x: x.end_date
    )
    next_payment = upcoming_loans[0] if upcoming_loans else None


    recent_payments = payments[:5]


    months_labels = []
    months_data   = []
    for i in range(5, -1, -1):
        month_start = (today.replace(day=1) - timedelta(days=30*i))
        month_name  = month_start.strftime('%b')
        month_total = sum(
            float(p.amount) for p in payments
            if p.date.year == month_start.year and p.date.month == month_start.month
        )
        months_labels.append(month_name)
        months_data.append(month_total)


    banks_labels = []
    banks_data   = []
    for loan in loans:
        banks_labels.append(loan.bank_name)
        banks_data.append(float(loan.remaining_amount()))

    # Курс валют
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
        'months_labels':   json.dumps(months_labels),
        'months_data':     json.dumps(months_data),
        'banks_labels':    json.dumps(banks_labels),
        'banks_data':      json.dumps(banks_data),
    })

