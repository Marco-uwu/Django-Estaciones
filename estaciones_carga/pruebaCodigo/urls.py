from django.urls import path
from . import views

urlpatterns = [
    path('grafica/', views.grafica_mediciones_view, name='grafica_mediciones'),
]
