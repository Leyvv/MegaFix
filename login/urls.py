# login/urls.py
from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('', views.authView, name='login'),  # Vista para el login
]
