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

def grafica_mediciones_view(request):
    id_estacion = 4  
    id_medicion = 9
    fecha_inicio = '2024-12-05 16:08:06'
    fecha_fin = '2024-12-05 16:08:45'

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

    # Configurar etiquetas y título
    ax.set(xlabel='Fecha', ylabel='Valor', title='Mediciones')

    # Rotar las etiquetas del eje X para mejor legibilidad
    plt.xticks(rotation=45)

    # Crear un objeto de bytes para guardar la imagen
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    # Convertir la imagen a base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')

    # Pasar la imagen al contexto de la plantilla
    context = {'image_base64': image_base64}
    return render(request, 'prueba.html', context)
