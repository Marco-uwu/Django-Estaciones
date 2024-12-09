from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.contrib import messages

import matplotlib.pyplot as plt
import io
from .models import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from datetime import datetime
import pytz
import base64

def prueba(request):
    if request.method == "POST":
        try:
            resultado = "Ok"
            messages.success(request, resultado)
        except Exception as e:
            resultado = "Error"
            messages.error(request, resultado)
    return render(request, "prueba.html")

def grafica_mediciones_view(request, id_estacion, id_medicion, fecha_inicio, fecha_fin):
    # Convertir las cadenas de fecha y hora a objetos datetime
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M:%S')

    # Filtrar las mediciones por id_estacion y el intervalo de fechas
    mediciones = Mediciones.objects.filter(id_estacion=id_estacion, fecha__range=[fecha_inicio, fecha_fin], id_tipo_medicion=id_medicion)

    # Extraer los valores de fecha y valor
    fechas = [medicion.fecha for medicion in mediciones]
    valores = [medicion.valor for medicion in mediciones]

    # Crear una figura y un eje
    fig, ax = plt.subplots()

    # Crear la gráfica
    ax.plot(fechas, valores)
    
    nombre_medicion = TiposMedicion.objects.values_list('descripcion', flat=True).get(id=id_medicion)

    # Configurar etiquetas y título
    ax.set(xlabel='Fecha', ylabel='Valor', title=nombre_medicion)

    # Rotar las etiquetas del eje X para mejor legibilidad
    plt.xticks(rotation=90)

    # Crear un objeto de bytes para guardar la imagen
    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)

    # Devolver la imagen como respuesta HTTP
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    response['Content-Length'] = str(len(response.content))
    return response
