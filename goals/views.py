from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Goal
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API')


def ask_groq(question):
    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {GROQ_API_KEY}',
                'Content-Type': 'application/json',
            },
            json={
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': 'You are a friendly financial advisor. Reply briefly in Russian, max 3 sentences.'},
                    {'role': 'user', 'content': question},
                ],
                'max_tokens': 200,
            },
            timeout=15
        )
        data = response.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f'AI unavailable: {str(e)[:50]}'


@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user)
    ai_answer = None

    if request.GET.get('ai_help'):
        question = request.GET.get('ai_help')
        ai_answer = ask_groq(question)

    return render(request, 'goals/goal_list.html', {
        'goals':     goals,
        'ai_answer': ai_answer,
    })


@login_required
def goal_create(request):
    if request.method == 'POST':
        title         = request.POST.get('title')
        description   = request.POST.get('description', '')
        target_amount = request.POST.get('target_amount')
        target_date   = request.POST.get('target_date')
        icon          = request.POST.get('icon', '🎯')

        if not title or not target_amount or not target_date:
            return render(request, 'goals/goal_form.html', {
                'error': 'Please fill all required fields!'
            })

        Goal.objects.create(
            user=request.user,
            title=title,
            description=description,
            target_amount=target_amount,
            target_date=target_date,
            icon=icon,
        )
        return redirect('goal_list')

    return render(request, 'goals/goal_form.html')


@login_required
def goal_update(request, pk):
    goal = Goal.objects.filter(pk=pk, user=request.user).first()
    if not goal:
        return redirect('goal_list')

    if request.method == 'POST':
        goal.title          = request.POST.get('title')
        goal.description    = request.POST.get('description', '')
        goal.target_amount  = request.POST.get('target_amount')
        goal.current_amount = request.POST.get('current_amount', 0)
        goal.target_date    = request.POST.get('target_date')
        goal.icon           = request.POST.get('icon', '🎯')
        goal.save()
        return redirect('goal_list')

    return render(request, 'goals/goal_form.html', {'goal': goal})


@login_required
def goal_delete(request, pk):
    goal = Goal.objects.filter(pk=pk, user=request.user).first()
    if not goal:
        return redirect('goal_list')

    if request.method == 'POST':
        goal.delete()
        return redirect('goal_list')

    return render(request, 'goals/goal_confirm_delete.html', {'goal': goal})
