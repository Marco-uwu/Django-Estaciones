from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import warnings
import paho.mqtt.client as mqtt
from .decorators import admin_required

@admin_required
def estadisticas(request):
    template = loader.get_template('index_estadisticas.html')
    estaciones = Estaciones.objects.all().values() 

    context = {
        'estaciones' : estaciones,
    }
    return HttpResponse(template.render(context, request))
