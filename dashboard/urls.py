from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('download-report/', views.download_report, name='download_report'),
    path('send-test-reminder/', views.send_test_reminder, name='send_test_reminder'),
    path('send-payment-reminder/', views.send_payment_reminder, name='send_payment_reminder'),
]
