from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import EmailConfirm

User = get_user_model()

def send_confirmation_code(user):
    code = randint(100000, 999999)
    EmailConfirm.objects.update_or_create(
        user=user,
        defaults={'code': str(code)}
    )
    send_mail(
        subject='Loan Tracker TJ — Confirm your email',
        message=f'Welcome {user.username}! Your confirmation code: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )

