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

    
        
        

