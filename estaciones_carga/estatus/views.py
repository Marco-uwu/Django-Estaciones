from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Estaciones, ParametrosMedicion

def estatus(request):
    estaciones = Estaciones.objects.all().values()
    template = loader.get_template('index_estatus.html')
    context = {
        'estaciones' : estaciones,
    }
    return HttpResponse(template.render(context, request))
