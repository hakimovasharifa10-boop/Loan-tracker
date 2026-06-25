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
    
    
@login_required
def payment_create(request):
    loans = Loan.objects.filter(user=request.user)

    if request.method == 'POST':
        loan_id = request.POST.get('loan')
        amount  = request.POST.get('amount')
        date    = request.POST.get('date')
        notes   = request.POST.get('notes')

        if not loan_id or not amount or not date:
            return render(request, 'payments/payment_form.html', {
                'error': 'All fields are required!',
                'loans': loans,
            })
            
        loan = Loan.objects.filter(pk=loan_id, user=request.user).first()
        if not loan:
            return redirect('payment_list')

        Payment.objects.create(
            user=request.user,
            loan=loan,
            amount=amount,
            date=date,
            notes=notes
        )
        return redirect('payment_list')

    return render(request, 'payments/payment_form.html', {
        'loans': loans,
    })
