# dash/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'dash'

urlpatterns = [
    path('', views.homeView, name='home'),  # Vista para el home del superusuario
    path('home2/', views.home2View, name='home2'),  # Vista para el home de los usuarios normales
   #  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('comparaciones/', views.comparaciones, name='comparaciones'),
    path('comparar_ventas/', views.comparar_ventas, name='comparar_ventas'),
  path('comparacion/', views.ver_comparacion, name='ver_comparacion'),
 path('datosEnero-Diciembre 2020-2024/<int:anio>/<str:mes>.html',
        views.ver_datos_mes,
        name='ver_datos_mes'),
 path('obtener-dia-mas-vendido/', views.obtener_dia_mas_vendido_filtrado, name='obtener_dia_mas_vendido'),
 path('resumen/', views.obtener_dia_mas_vendido, name='resumen_datos'),  
]
