# login/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.authView, name='login'),  # Vista para el login
]
