from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from .form import PaymentForm


@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user)
    loans    = request.user.loans.all()
    selected_loan = request.GET.get('loan', '')

    if selected_loan:
        payments = payments.filter(loan__id=selected_loan)

    total = sum(p.amount for p in payments)

    return render(request, 'payments/payment_list.html', {
        'payments':      payments,
        'loans':         loans,
        'selected_loan': selected_loan,
        'total':         total,
    })


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            
            loan=payment.loan
            
            if loan.remaining_amount() <=0:
                loan.status = 'closed'
                loan.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(user=request.user)

    return render(request, 'payments/payment_form.html', {'form': form})


@login_required
def payment_update(request, pk):
    payment = Payment.objects.filter(pk=pk, user=request.user).first()
    if not payment:
        return redirect('payment_list')

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment, user=request.user)
        if form.is_valid():
            payment=form.save()
            
            loan=payment.loan
            
            if loan.remaining_amount() <=0:
                loan.status = 'closed'
            else:
                loan.status = 'active'
            loan.save()
            
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment, user=request.user)

    return render(request, 'payments/payment_form.html', {
        'form':    form,
        'payment': payment,
    })


@login_required
def payment_delete(request, pk):
    payment = Payment.objects.filter(pk=pk, user=request.user).first()
    if not payment:
        return redirect('payment_list')

    if request.method == 'POST':
        payment.delete()
        return redirect('payment_list')

    return render(request, 'payments/payment_confirm_delete.html', {'payment': payment})