# dash/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dash.templates.Graficas.comp import generar_html_comparacion
from django.http import Http404

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
    
def ver_datos_mes(request, anio, mes):
    template = f'datosEnero-Diciembre 2020-2024/{anio}/{mes}.html'
    return render(request, template)

def ver_comparacion(request):
    año = request.GET.get("año")
    mes = request.GET.get("mes")
    # Podrías redirigir o renderizar directamente una plantilla con esos datos
    return render(request, f'datosEnero-Diciembre 2020-2024/{año}/{mes}.html')


    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                DAY(fecha) AS dia,
                DAYNAME(fecha) AS dia_semana,
                gran_total
            FROM ventas
            WHERE fecha BETWEEN '2020-01-02' AND '2020-01-31'
            ORDER BY gran_total DESC
            LIMIT 1
        """)
        resultado = cursor.fetchone()
        if resultado:
            dia, dia_semana, cantidad = resultado
        else:
            dia, dia_semana, cantidad = None, None, None
    
    print(resultado)

    return render(request, 'datosEnero-Diciembre 2020-2024/2020/agosto.html', {
        'dia': dia,
        'dia_semana': dia_semana,
        'cantidad': cantidad
    })

