# dash/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from dash.templates.Graficas.comp import generar_html_comparacion

@login_required
def homeView(request):
    return render(request, 'dash/home.html')  # Redirige a home.html para superusuarios

@login_required
def home2View(request):
    return render(request, 'dash/home2.html')  # Redirige a home2.html para usuarios normales

def comparaciones(request):
    return render(request, 'dash/comparaciones.html')
def grafica_2020(request):
    return render(request, 'dash/grafica_2020.html')

def comparar_ventas(request):
    year1 = int(request.GET.get('year1', 2022))
    year2 = int(request.GET.get('year2', 2023))

    try:
        generar_html_comparacion(year1, year2)
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



