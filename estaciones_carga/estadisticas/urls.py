from django.urls import path
from . import views

urlpatterns = [
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
]
