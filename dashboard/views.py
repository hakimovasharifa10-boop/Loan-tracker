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
