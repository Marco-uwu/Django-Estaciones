from django.urls import path
from . import views

urlpatterns = [
    path('parametros/', views.parametros, name='parametros'),
]
