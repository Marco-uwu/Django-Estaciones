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
import base64
import re
from django.db import transaction, IntegrityError

def procesar_mac(mac_str):
    # Validar que la dirección MAC esté en el formato "00:11:22:33:44:55"
    if not re.match(r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$', mac_str):
        return None

    # Convertir la dirección MAC al formato continuo sin los ":" y en mayúsculas
    dir_mac = mac_str.replace(":", "").upper()

    # Codificar la dirección MAC en Base64
    mac_bytes = dir_mac.encode('utf-8')
    mac_base64 = base64.urlsafe_b64encode(mac_bytes).decode('utf-8')
    return mac_base64

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
    
    tarifas = Tarifas.objects.all().order_by('id')
    reglas = ReglasMedicion.objects.all().order_by('id')

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
        elif tipo_formulario == "3":
            nuevo_nombre = request.POST.get('nombre_nueva_estacion')
            nueva_dir = procesar_mac(request.POST.get('dir_nueva_estacion'))

            if nueva_dir is not None:
                try:
                    with transaction.atomic():
                        if not Estaciones.objects.filter(dir_mac=nueva_dir).exists():
                            id_regla_instancia = ReglasMedicion.objects.get(pk=1)
                            id_tarifa_instancia = Tarifas.objects.get(pk=1)
                            nueva_estacion = Estaciones(
                                id_regla=id_regla_instancia,
                                nombre=nuevo_nombre,  # Asegúrate de que 'nuevo_nombre' esté definido
                                estado='Fuera de servicio',
                                dir_mac=nueva_dir,
                                id_tarifa=id_tarifa_instancia
                            )
                            nueva_estacion.save()
                            resultado = "Estación insertada exitosamente."
                        else:
                            resultado = "Ya existe una estación con la dirección MAC especificada."
                except IntegrityError:
                    resultado = "Ocurrió un error al intentar insertar la estación."
            else:
                resultado = "Error: La dirección MAC no está en el formato solicitado. Use 00:11:22:33:44:55."
        elif tipo_formulario == "4":
            id_estacion_modificar = int(request.POST.get('id_estacion'))
            registro_estacion = Estaciones.objects.get(pk=id_estacion_modificar)
            #resultado = str(registro_estacion.nombre)
        elif tipo_formulario == "5":
            mac_existe = None
            id_regla_form = request.POST.get('nueva_regla')
            id_tarifa_form = request.POST.get('nueva_tarifa')
            id_estacion_form = request.POST.get('id_estacion_modificar')
            dir_estacion_form = request.POST.get('nueva_direccion', None)
            if dir_estacion_form is not "":
                nueva_dir = procesar_mac(dir_estacion_form)

            try:
                with transaction.atomic():
                    id_regla_instancia = ReglasMedicion.objects.get(pk=id_regla_form)
                    id_tarifa_instancia = Tarifas.objects.get(pk=id_tarifa_form)
                            
                    estacion = Estaciones.objects.get(pk=id_estacion_form)

                    estacion.nombre = request.POST.get('nuevo_nombre_estacion')
                    estacion.ubicacion = request.POST.get('nueva_ubicacion')
                    estacion.estado = request.POST.get('nuevo_estado')
                    estacion.id_regla = id_regla_instancia
                    estacion.id_tarifa = id_tarifa_instancia
                    if dir_estacion_form is not "":
                        if not Estaciones.objects.filter(dir_mac=nueva_dir).exists():
                            estacion.dir_mac = nueva_dir
                        else:
                            mac_existe = "Ya existe una estación con la dirección MAC especificada."
                        
                    if estacion.dir_mac is not None and mac_existe is None:
                        estacion.save()
                        resultado = "Cambios guardados exitosamente! :)"
                    elif mac_existe is not None:
                        resultado = mac_existe
                    else:
                        resultado = f"Error: La dirección MAC no está en el formato solicitado. Use 00:11:22:33:44:55."
            except IntegrityError:
                resultado = "Ocurrió un error al intentar actualizar la estación."
        elif tipo_formulario == "6":
            id_estacion_eliminar = request.POST.get('id_estacion_eliminar')
            try:
                estacion_eliminar = Estaciones.objects.get(id=id_estacion_eliminar)
                estacion_eliminar.delete()
                resultado = "Estacion eliminada exitosamente"
            except IntegrityError:
                resultado = "Ocurrió un error al tratar de eliminar la Estación. Verifica que no tenga mediciones."
        else:
            resultado = "Error en solicitud POST"
    
    
    paginator = Paginator(mediciones, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'request' : request,
        'estaciones' : estaciones,
        'resultado' : resultado,
        'page_obj' : page_obj,
        'tarifas' : tarifas,
        'reglas' : reglas,
    }
    return HttpResponse(template.render(context, request))
