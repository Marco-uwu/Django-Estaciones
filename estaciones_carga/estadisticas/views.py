from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import warnings
import paho.mqtt.client as mqtt
from .decorators import admin_required
from django.db import transaction, IntegrityError

import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime
import pytz
import base64

from reportlab.pdfgen import canvas

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
        elif tipo_formulario == "4":
            mensaje = ""             
        elif tipo_formulario == "5":
            nueva_descipcion = request.POST.get('descripcion_tarifa')
            nuevo_precio = request.POST.get('precio_tarifa')
            nueva_moneda = request.POST.get('moneda_tarifa')
            
            try:
                with transaction.atomic():
                    nueva_tarifa = Tarifas(
                                    descripcion= nueva_descipcion,
                                    precio=nuevo_precio,
                                    moneda=nueva_moneda
                                )
                    nueva_tarifa.save()
                    mensaje = "Tarifa creada exitosamente!"
            except IntegrityError:
                mensaje = "Ocurrió un error al crear la tarifa."
        elif tipo_formulario == "6":
            id_tarifa_eliminar = request.POST.get('id_tarifa_eliminar')
            try:
                tarifa = Tarifas.objects.get(id=id_tarifa_eliminar)
                tarifa.delete()
                mensaje = "Tarifa eliminada exitosamente"
            except IntegrityError:
                mensaje = "Ocurrió un error al tratar de eliminar la tarifa, verifica que no esté asignada a una estación."
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

def generar_pdf(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        dato_id = request.POST.get('id_sesion_recibo')
        dato = SesionesCarga.objects.get(id=dato_id)
        fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M")
        tiempo_total = (dato.fecha_fin - dato.fecha_inicio)
        segundos_totales = tiempo_total.total_seconds()
        tiempo_decimal = segundos_totales / 3600
        horas, resto = divmod(int(segundos_totales), 3600)
        minutos, segundos = divmod(resto, 60)
        
        mediciones_potencia = Mediciones.objects.filter(id_estacion=dato.id_estacion.id, fecha__range=[dato.fecha_inicio, dato.fecha_fin], id_tipo_medicion=9)
        
        precio_total = ((float(mediciones_potencia[0].valor) * tiempo_decimal)/1000) * float(dato.id_estacion.id_tarifa.precio)
        precio_total = round(precio_total, 2)

        # Crear un objeto HttpResponse con el tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        # Crear un objeto canvas
        p = canvas.Canvas(response)
        
        p.drawString(50, 800, f"------------------------------------------------------------------------------------------------------------------")
        p.drawString(50, 775, f"|                                              ESTACIONES DE CARGA                                              |")
        p.drawString(50, 750, f"------------------------------------------------------------------------------------------------------------------")
        p.drawString(50, 790, f"|                                                                                                                                       |")
        p.drawString(50, 760, f"|                                                                                                                                       |")
        # Coordenada inicial
        x = 100
        y = 725

        # Escribir datos en el PDF
        p.drawString(x, y, f"Fecha: {fecha_actual}")
        y -= 40
        p.drawString(x, y, f"ID Estacion:")
        y -= 20
        p.drawString(x, y, f"Estacion:")
        y -= 20
        p.drawString(x, y, f"Tarifa por kWh:")
        y -= 40
        p.drawString(x, y, f"Hora de inicio:")
        y -= 20
        p.drawString(x, y, f"Hora de fin:")
        y -= 20
        p.drawString(x, y, f"Tiempo total de carga:")
        y -= 20
        p.drawString(50, y, f"------------------------------------------------------------------------------------------------------------------")
        y -= 20
        p.drawString(x, y, f"TOTAL:")
        
        x = 250
        y = 725
        p.drawString(x, y, "")
        y -= 40
        p.drawString(x, y, f"{dato.id_estacion.id}")
        y -= 20
        p.drawString(x, y, f"\"{dato.id_estacion.nombre}\"")
        y -= 20
        p.drawString(x, y, f"$ {dato.id_estacion.id_tarifa.precio} {dato.id_estacion.id_tarifa.moneda}")
        y -= 40
        p.drawString(x, y, f"{dato.fecha_inicio}")
        y -= 20
        p.drawString(x, y, f"{dato.fecha_fin}")
        y -= 20
        p.drawString(x, y, f"{horas:02}:{minutos:02}:{segundos:02}")
        y -= 40
        p.drawString(x, y, f"$ {precio_total} {dato.id_estacion.id_tarifa.moneda} ")

        # Finalizar el PDF
        p.showPage()
        p.save()
        return response
    else:
        return HttpResponseBadRequest("<h1>400 Bad Response</h1><p>Verifica tu solicitud</p>")
