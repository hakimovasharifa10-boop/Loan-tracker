from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Payment
from .forms import PaymentForm


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
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
            form.save()
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment, user=request.user)

    return render(request, 'payments/payment_form.html', {
        'form':    form,
        'payment': payment,
    })