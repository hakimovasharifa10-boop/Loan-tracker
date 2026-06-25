from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from loans.models import Loan

@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)

    loan_id = request.GET.get('loan')
    if loan_id:
        payments = payments.filter(loan__id=loan_id)

    
    loans = Loan.objects.filter(user=request.user)


    total = sum(p.amount for p in payments)
    
    return render(request, 'payments/payment_list.html', {
        'payments':      payments,
        'loans':         loans,
        'total':         total,
        'selected_loan': loan_id,
    })
