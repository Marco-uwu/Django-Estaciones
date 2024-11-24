from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Estaciones, ParametrosMedicion
import warnings
import paho.mqtt.client as mqtt

def enviar_apagado_manual(direccion, nombre):
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    try:
        # Crear una instancia del cliente MQTT
        clienteMqtt = mqtt.Client()
        clienteMqtt.connect("localhost", 1883, 60)

        # Construir el tema y el mensaje
        tema = f"estaciones/alertas/{direccion}/shutdown"
        mensaje = ">> Apagado manual"

        # Publicar el mensaje
        clienteMqtt.publish(tema, mensaje)

        # Cerrar la conexión MQTT
        clienteMqtt.disconnect()

        return (f"¡{nombre} apagada correctamente! {direccion}")
    except Exception as e:
        return (f"Error al intentar apagar \"{nombre}\" ")

def estatus(request):
    template = loader.get_template('index_estatus.html')
    estaciones = Estaciones.objects.all().values()
    resultado = ""
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
    }
    return HttpResponse(template.render(context, request))
