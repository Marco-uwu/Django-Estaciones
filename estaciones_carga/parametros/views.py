from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Estaciones, ParametrosMedicion

def parametros(request):
    parametros = ParametrosMedicion.objects.filter(id_regla=1)
    template = loader.get_template('index_parametros.html')
    context = {
        'parametros' : parametros,
    }
    return HttpResponse(template.render(context, request))
