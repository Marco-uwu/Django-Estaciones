from django.urls import path
from . import views

urlpatterns = [
    path('estatus/', views.estatus, name='estatus'),
]
