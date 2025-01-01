from django.urls import path
from . import views


urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('choose_parkeges/', views.choose_location, name='choose_parkeges'),
    path('processing_payments/', views.payment_processing, name='processing_payments'),
    path('user_payment_history/', views.user_payment_history, name='user_payment_history'),
]
