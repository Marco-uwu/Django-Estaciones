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

    estacion_mediciones = request.GET.get('estacion_medicion', '')

    if estacion_mediciones:
        mediciones = Mediciones.objects.filter(id_estacion=estacion_mediciones)[:100]
    else:
        mediciones = Mediciones.objects.all()[:100]

    # Configurar el paginador para 10 registros por página
    paginator = Paginator(mediciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        nombre = request.POST.get("nombre_estacion")
        direccion =  request.POST.get("dir_estacion")
        try:
            resultado = enviar_apagado_manual(direccion, nombre)
        except Exception as e:
            resultado = "Error al apagar " + nombre
    context = {
        'estaciones' : estaciones,
        'resultado' : resultado,
        'page_obj' : page_obj,
    }
    return HttpResponse(template.render(context, request))
