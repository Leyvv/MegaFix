# truper_insights/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),  # Incluir las URLs de la app 'login'
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', include('dash.urls')),   # Incluir las URLs de la app 'dash'
    path('', lambda request: redirect('login:login')),  # Redirige la raíz a la página de login
]
