# dash/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from dash.templates.Graficas.comp import generar_html_comparacion
from django.http import Http404
from django.template.loader import render_to_string

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


def obtener_dia_mas_vendido_filtrado(request):
    anio = request.GET.get('año')
    mes = request.GET.get('mes')

    # Mapeo de nombres de mes en español a número
    meses = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }

    mes_num = meses.get(mes.lower(), '01')

    ruta = r'C:\Users\jazmi\Documents\GitHub\MegaFix\dias_mas_vendidos.txt'
    dia_mas_vendido = 'Desconocido'
    total_mayor = 0.0

    try:
        with open(ruta, 'r', encoding='utf-8') as file:
            next(file)  # Saltar encabezado
            for linea in file:
                partes = linea.strip().split('\t')
                if len(partes) == 2:
                    fecha, total_str = partes
                    if fecha.startswith(f"{anio}-{mes_num}"):
                        total = float(total_str.replace('$', '').replace(',', ''))
                        if total > total_mayor:
                            total_mayor = total
                            dia_mas_vendido = fecha
    except Exception:
        dia_mas_vendido = 'Error'
        total_mayor = 0.0

    html = render_to_string('dash/resumen_datos.html', {
        'dia_mayor': dia_mas_vendido,
        'valor_mayor': f"${total_mayor:,.2f}"
    })

    return JsonResponse({'html': html})

def obtener_dia_mas_vendido(request):
    # Carga el día y total desde el archivo
    # Aquí deberías leer el archivo y aplicar los filtros si hay mes y año
    # ...
    context = {
        'dia_mayor': '2024-04-05',
        'valor_mayor': '$303,544.90'
    }
    return render(request, 'dash/resumen_datos.html', context)