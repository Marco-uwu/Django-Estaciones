from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
import warnings
import paho.mqtt.client as mqtt
from .decorators import admin_required
from .claseEstacion import Estacion

def enviar_apagado_manual(direccion, nombre):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    try:
        # Crear una instancia del cliente MQTT
        clienteMqtt = mqtt.Client()
        clienteMqtt.connect("localhost", 1883, 60)

        # Construir el tema y el mensaje
        tema = f"estaciones/alertas/{direccion}/shutdown"
        estacion = Estacion(direccion)
        mensaje = estacion.to_bytearray()

        # Publicar el mensaje
        clienteMqtt.publish(tema, mensaje)

        # Cerrar la conexión MQTT
        clienteMqtt.disconnect()

        return (f"¡{nombre} apagada correctamente!")
    except Exception as e:
        return (f"Error al intentar apagar \"{nombre}\" ")

@admin_required
def estatus(request):
    template = loader.get_template('index_estatus.html')
    estaciones = Estaciones.objects.all().values()
    resultado = ""

    mediciones = Mediciones.objects.all().order_by('id')
    page_number = request.GET.get('page')

    if request.method == "POST":
        tipo_formulario = request.POST.get('id_formulario')

        # Ejecutar según tipo de solicitud
        if tipo_formulario == "1": # Solicitud de filtrado de tabla

            nombre = request.POST.get("nombre_estacion")
            direccion =  request.POST.get("dir_estacion")
            try:
                resultado = enviar_apagado_manual(direccion, nombre)
            except Exception as e:
                resultado = "Error al apagar " + nombre
        elif tipo_formulario == "2":
            estacion_id = request.POST.get('estacion')
            pagina = request.POST.get('pagina', None)
            if estacion_id:
                mediciones = Mediciones.objects.filter(id_estacion=estacion_id).order_by('id')
            if pagina:
                page_number = int(pagina)
            else:
                page_number = 1
        else:
            resultado = "Error en solicitud POST"
    
    
    paginator = Paginator(mediciones, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'request' : request,
        'estaciones' : estaciones,
        'resultado' : resultado,
        'page_obj' : page_obj,
    }
    return HttpResponse(template.render(context, request))
