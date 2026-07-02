from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from loans.models import Loan
from payments.models import Payment
from datetime import timedelta
import requests
import json
from django.http import HttpResponse
from reportlab.pdfgen import canvas



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
    total_debt  = sum(loan.remaining_amount() for loan in loans)
    total_paid  = sum(p.amount for p in payments)
    active_loans  = loans.count()


    overdue_loans = [loan for loan in loans if loan.end_date < today]

    
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
    
    
@login_required
def download_report(request):
    loans=Loan.objects.filter(user=request.user)
    payments=Payment.objects.filter(user=request.user)
    
    total_debt=sum(loan.remaining_amount() for loan in loans)
    total_paid=sum(payment.amount for payment in payments)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=loan_report_pdf'
    
    p=canvas.Canvas(response)
    
    p.setFont("Helvetica",12)
    p.drawString(50,760,f"User:{request.user.username}")
    p.drawString(50,740,f"Email:{request.user.email}")
    p.drawString(50,710,f"Total debt:{total_debt} TJS")
    p.drawString(50,760,f"Total paid:{total_paid} TJS")
    
    y=650
    
    p.setFont('Helvetica',11)
    
    for loan in loans:
        p.drawString(50,y,f"Bank:{loan.bank_name}")
        y=-20
        p.drawString(70,y,f"Amount:{loan.amount} TJS")
        y=-20
        p.drawString(70,y,f"Rate:{loan.interest_rate} %")
        y=-20
        p.drawString(70,y,f"Monthly payment:{loan.monthly_payment} TJS")
        y=-20
        p.drawString(50,y,f"Remaining:{loan.remaining_amount()} TJS")
        y=-30
        
        if y < 80:
            p.showPage()
            y=800
            p.setFont("Helvetica",11)
            
    p.showPage()
    p.save()
    
    return response
        
    
    
