from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dash.templates.Graficas.comp import generar_html_comparacion
from django.http import Http404
from django.template.exceptions import TemplateDoesNotExist

@login_required
def homeView(request):
    return render(request, 'dash/home.html')

@login_required
def home2View(request):
    return render(request, 'dash/home2.html')

def comparaciones(request):
    return render(request, 'dash/comparaciones.html')

def predicciones(request):
    return render(request, 'dash/predicciones.html')

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

def ver_datos_mes(request, anio, mes):
    template = f'datosEnero-Diciembre 2020-2024/{anio}/{mes}.html'
    return render(request, template)

def ver_comparacion(request):
    año = request.GET.get("año")
    mes = request.GET.get("mes")

    if not año or not mes:
        return render(request, 'error.html', {'mensaje': 'Año o mes no proporcionado'})

    template_name = f'datosEnero-Diciembre 2020-2024/{año}/{mes}.html'

    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        return render(request, 'error.html', {'mensaje': f'La plantilla {template_name} no se encontró'})


def ver_comparacion_anual(request):
    año = request.GET.get('año')

    if not año:
        return render(request, 'error.html', {'mensaje': 'Año no proporcionado'})

    template_name = f'datosAnualidad/{año}.html'

    try:
        return render(request, template_name)
    except TemplateDoesNotExist:
        return render(request, 'error.html', {'mensaje': f'La plantilla para el año {año} no se encontró'})
