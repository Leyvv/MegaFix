# dash/urls.py
from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    path('', views.homeView, name='home'),  # Vista para el home del superusuario
    path('home2/', views.home2View, name='home2'),  # Vista para el home de los usuarios normales
    path('comparaciones/', views.comparaciones, name='comparaciones'),
    path('comparar_ventas/', views.comparar_ventas, name='comparar_ventas'),
    path('comparacion/', views.ver_comparacion, name='ver_comparacion'),
    path('ver_comparacion_anual/', views.ver_comparacion_anual, name='ver_comparacion_anual'),
    path('datosEnero-Diciembre 2020-2024/<int:anio>/<str:mes>.html',
         views.ver_datos_mes,
         name='ver_datos_mes'),
]

