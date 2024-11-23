from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Estaciones, ParametrosMedicion
from django.contrib import messages

def estatus(request):
    template = loader.get_template('index_estatus.html')
    estaciones = Estaciones.objects.all().values()
    resultado = ""
    if request.method == "POST":
        nombre = request.POST.get("nombre_estacion")
        try:
            resultado = "Ok " + nombre
            messages.success(request, resultado)
        except Exception as e:
            resultado = "Error"
            messages.error(request, resultado)
    context = {
        'estaciones' : estaciones,
        'resultado' : resultado,
    }
    return HttpResponse(template.render(context, request))
