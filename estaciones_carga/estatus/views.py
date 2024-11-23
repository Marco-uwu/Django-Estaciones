from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Estaciones, ParametrosMedicion
from django.contrib import messages

def estatus(request):
    template = loader.get_template('index_estatus.html')
    estaciones = Estaciones.objects.all().values()
    if request.method == "POST":
        try:
            resultado = "Ok"
            messages.success(request, resultado)
        except Exception as e:
            resultado = "Error"
            messages.error(request, resultado)
    context = {
        'estaciones' : estaciones,
    }
    return HttpResponse(template.render(context, request))
