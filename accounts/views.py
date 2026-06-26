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
    
def register_view(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        email     = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not password1:
            return render(request, 'accounts/register.html', {'error': 'All fields are required!'})
        elif password1 != password2:
            return render(request, 'accounts/register.html', {'error': 'Passwords do not match!'})
        elif User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': 'Username already exists!'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'accounts/register.html', {'error': 'Email already exists!'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            is_active=False
        )
        send_confirmation_code(user)
        return render(request, 'accounts/confirm.html', {'user': user})

    return render(request, 'accounts/register.html')

def confirm_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code  = request.POST.get('code')

        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'accounts/confirm.html', {'error': 'Incorrect email!'})

        try:
            email_confirm = EmailConfirm.objects.get(user=user)
        except EmailConfirm.DoesNotExist:
            return render(request, 'accounts/confirm.html', {'error': 'Code not found!'})

        if code != email_confirm.code:
            return render(request, 'accounts/confirm.html', {'error': 'Incorrect code!'})
        
        user.is_active = True
        user.save()
        return redirect('login')

    return render(request, 'accounts/confirm.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'accounts/login.html', {'error': 'All fields are required!'})

        user = authenticate(request, username=username, password=password)
        if not user:
            return render(request, 'accounts/login.html', {'error': 'Incorrect login or password!'})

        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name  = request.POST.get('last_name', '')
        user.phone      = request.POST.get('phone', '')
        user.address    = request.POST.get('address', '')
        if request.FILES.get('avatar'):
            user.avatar = request.FILES.get('avatar')
        user.save()
        return redirect('profile')
    return render(request, 'accounts/profile.html')
