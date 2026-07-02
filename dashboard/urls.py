from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('download-report/', views.download_report, name='download_report'),
]

