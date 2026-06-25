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

    
        
        

