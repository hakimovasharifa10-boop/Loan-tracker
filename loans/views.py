from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Loan
from groq import Groq
import requests
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API'))

def get_exchange_rates():
    try:
        response = requests.get('https://api.exchangerate-api.com/v4/latest/TJS', timeout=5)
        data = response.json()
        return {
            'USD': round(data['rates']['USD'], 4),
            'RUB': round(data['rates']['RUB'], 2),
            'EUR': round(data['rates']['EUR'], 4),
        }
    except:
        return {'USD': 0.092, 'RUB': 8.5, 'EUR': 0.085}
    
@login_required
def loan_list(request):
    loans = Loan.objects.filter(user=request.user)
    today = timezone.now().date()

    
    overdue_loans = [loan for loan in loans if loan.end_date < today]

    
    ai_answer = None
    question  = request.GET.get('ai_help', '').strip()
    if question:
        loans_for_ai = []
        for loan in loans:
            loans_for_ai.append(
                f"- {loan.bank_name} | Amount: {loan.amount} TJS | "
                f"Rate: {loan.interest_rate}% | Monthly: {loan.monthly_payment} TJS | "
                f"Remaining: {loan.remaining_amount()} TJS | "
                f"End date: {loan.end_date}"
            )

        loans_text = '\n'.join(loans_for_ai) if loans_for_ai else 'No loans yet.'

        prompt = f'''You are a helpful financial advisor for citizens of Tajikistan.
The user has these loans:
{loans_text}
Give a short and specific advice in 3-5 sentences.
Tell which loan to pay first and why.
Be specific with numbers.'''

        response = client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': prompt},
                {'role': 'user',   'content': question}
            ],
            model='llama-3.3-70b-versatile'
        )
        ai_answer = response.choices[0].message.content

    rates = get_exchange_rates()
    
    return render(request, 'loans/loan_list.html', {
        'loans':         loans,
        'overdue_loans': overdue_loans,
        'ai_answer':     ai_answer,
        'rates':         rates,
        'today':         today,
    })
    
@login_required
def loan_create(request):
    if request.method == 'POST':
        bank_name       = request.POST.get('bank_name')
        amount          = request.POST.get('amount')
        interest_rate   = request.POST.get('interest_rate')
        monthly_payment = request.POST.get('monthly_payment')
        start_date      = request.POST.get('start_date')
        end_date        = request.POST.get('end_date')
        notes           = request.POST.get('notes')
        logo            = request.FILES.get('logo')

        if not bank_name or not amount or not interest_rate or not monthly_payment or not start_date or not end_date:
            return render(request, 'loans/loan_form.html', {
                'error': 'All fields are required!'
            })
            
        Loan.objects.create(
            user=request.user,
            bank_name=bank_name,
            amount=amount,
            interest_rate=interest_rate,
            monthly_payment=monthly_payment,
            start_date=start_date,
            end_date=end_date,
            notes=notes,
            logo=logo
        )
        return redirect('loan_list')

    return render(request, 'loans/loan_form.html')

@login_required
def loan_update(request, pk):
    loan = Loan.objects.filter(pk=pk, user=request.user).first()
    if not loan:
        return redirect('loan_list')

    if request.method == 'POST':
        bank_name       = request.POST.get('bank_name')
        amount          = request.POST.get('amount')
        interest_rate   = request.POST.get('interest_rate')
        monthly_payment = request.POST.get('monthly_payment')
        start_date      = request.POST.get('start_date')
        end_date        = request.POST.get('end_date')
        notes           = request.POST.get('notes')
        logo            = request.FILES.get('logo')

        if not bank_name or not amount or not interest_rate or not monthly_payment or not start_date or not end_date:
            return render(request, 'loans/loan_form.html', {
                'error': 'All fields are required!',
                'loan':  loan
            })
            
            
        loan.amount          = amount
        loan.interest_rate   = interest_rate
        loan.monthly_payment = monthly_payment
        loan.start_date      = start_date
        loan.end_date        = end_date
        loan.notes           = notes
        if logo:
            loan.logo = logo
        loan.save()
        return redirect('loan_list')

    return render(request, 'loans/loan_form.html', {'loan': loan})


@login_required
def loan_delete(request, pk):
    loan = Loan.objects.filter(pk=pk, user=request.user).first()
    if not loan:
        return redirect('loan_list')

    if request.method == 'POST':
        loan.delete()
        return redirect('loan_list')

    return render(request, 'loans/loan_confirm_delete.html', {'loan': loan})


    
        
        

