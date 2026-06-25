from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.conf import settings
from random import randint
from .models import EmailConfirm

User = get_user_model()

