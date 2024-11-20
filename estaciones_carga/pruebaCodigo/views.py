from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib import messages

def prueba(request):
    if request.method == "POST":
        try:
            resultado = "Ok"
            messages.success(request, resultado)
        except Exception as e:
            resultado = "Error"
            messages.error(request, resultado)
    return render(request, "prueba.html")
