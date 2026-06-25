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
    # Берём актуальный курс валют
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

    
        
        

