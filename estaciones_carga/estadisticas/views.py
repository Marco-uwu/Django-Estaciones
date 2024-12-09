from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import warnings
import paho.mqtt.client as mqtt
from .decorators import admin_required

import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime
import pytz
import base64

@admin_required
def estadisticas(request):
    template = loader.get_template('index_estadisticas.html')
    sesiones = SesionesCarga.objects.all().order_by('fecha_fin')
    num_sesiones = sesiones.count()
    estaciones = Estaciones.objects.all()
    tarifas = Tarifas.objects.all().order_by('id')
    registro_tarifa = ""
    mensaje = ""
    image_base64 = ""

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
        elif tipo_formulario == "4":
            id_estacion_grafica = request.POST.get('id_estacion_grafica')
            id_medicion_grafica = request.POST.get('id_medicion_grafica')
            fecha_inicio_grafica = request.POST.get('fecha_inicio_grafica')
            fecha_fin_grafica = request.POST.get('fecha_fin_grafica')


            fecha_inicio_grafica = datetime.strptime(fecha_inicio_grafica, '%Y-%m-%d %H:%M:%S')
            fecha_fin_grafica = datetime.strptime(fecha_fin_grafica, '%Y-%m-%d %H:%M:%S')
            mediciones = Mediciones.objects.filter(id_estacion=id_estacion_grafica, fecha__range=[fecha_inicio_grafica, fecha_fin_grafica], id_tipo_medicion=id_medicion_grafica)

            fechas = [medicion.fecha for medicion in mediciones]
            valores = [medicion.valor for medicion in mediciones]

            fig, ax = plt.subplots()
            ax.plot(fechas, valores)
            ax.set(xlabel='Fecha', ylabel='Valor', title='Mediciones')
            plt.xticks(rotation=45)

            # Crear un objeto de bytes para guardar la imagen
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)

            # Convertir la imagen a base64
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        else:
            mensaje = "Error: Solicitud POST inválida"

    context = {
        'mensaje' : mensaje,
        'sesiones' : sesiones,
        'estaciones' : estaciones,
        'request' : request,
        'num_sesiones' : num_sesiones,
        'tarifas' : tarifas,
        'grafica' : image_base64,
    }
    return HttpResponse(template.render(context, request))
