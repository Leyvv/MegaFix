# login/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect  

# Vista de login
@csrf_protect
def authView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                # Si es superusuario, redirige al home del superusuario
                return redirect('dash:home')  # Usamos 'dash:home' para hacer la redirección
            else:
                # Si no es superusuario, redirige al home del usuario normal
                return redirect('dash:home2')  # Usamos 'dash:home2' para hacer la redirección
        else:
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('login:login')  # Redirige al login si las credenciales son incorrectas
    
    return render(request, 'login/login.html')  # Renderiza el formulario de login si el método no es POST
