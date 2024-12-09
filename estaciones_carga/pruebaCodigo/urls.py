from django.urls import path
from . import views

urlpatterns = [
    path('prueba/', views.prueba, name='prueba'),
    path('grafica/<int:id_estacion>/<int:id_medicion>/<str:fecha_inicio>/<str:fecha_fin>/', views.grafica_mediciones_view, name='grafica_mediciones'),
]
