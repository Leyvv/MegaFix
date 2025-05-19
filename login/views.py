# login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect  
import jwt
from django.conf import settings
from datetime import datetime, timedelta

# Función auxiliar para generar el token
def generate_jwt(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(hours=1),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

@csrf_protect
def authView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            # ✅ Generar y guardar el token en la sesión
            token_generado = generate_jwt(user)
            request.session['jwt_token'] = token_generado
            print("TOKEN GUARDADO:", request.session.get('jwt_token'))

            if user.is_superuser:
                return redirect('dash:home')
            else:
                return redirect('dash:home2')
        else:
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('login:login')
    
    return render(request, 'login/login.html')