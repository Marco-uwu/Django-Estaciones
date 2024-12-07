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
    sesiones = SesionesCarga.objects.all().order_by('fecha_fin')
    num_sesiones = sesiones.count()
    estaciones = Estaciones.objects.all()
    tarifas = Tarifas.objects.all().order_by('id')
    registro_tarifa = ""
    mensaje = ""

    if request.method == "POST":
        # Verificar el tipo de formulario de la solicitud POST
        tipo_formulario = request.POST.get('id_formulario')
        
        # Ejecutar según tipo de solicitud
        if tipo_formulario == "1": # Solicitud de filtrado de tabla
            estacion_id = request.POST.get('estacion')
            if estacion_id:
                sesiones = sesiones.filter(id_estacion__id=estacion_id).order_by('fecha_fin')
        elif tipo_formulario == "2":
            tarifa_id = request.POST.get('tarifa')
            if tarifa_id:
                registro_tarifa = tarifas.filter(id= tarifa_id)[0]
        elif tipo_formulario == "3":
            tarifa_id = request.POST.get('tarifa')
            tarifa = Tarifas.objects.get(id=tarifa_id)
            tarifa.descripcion = request.POST.get('descripcion_tarifa')
            tarifa.precio = request.POST.get('precio_tarifa')
            tarifa.moneda = request.POST.get('moneda_tarifa')
            tarifa.save()
            mensaje = "Cambios guardados correctamente!"
        else:
            mensaje = "Error: Solicitud POST inválida"

    context = {
        'mensaje' : mensaje,
        'sesiones' : sesiones,
        'estaciones' : estaciones,
        'request' : request,
        'num_sesiones' : num_sesiones,
        'tarifas' : tarifas,
    }
    return HttpResponse(template.render(context, request))
