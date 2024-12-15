from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .decorators import admin_required

@admin_required
def reportes(request):

    reportes = Reportes.objects.all().order_by('id')
    estaciones = Estaciones.objects.all()

    page_number = 1
    
    if request.method == "POST":
        tipo_formulario = request.POST.get('id_formulario')
        if tipo_formulario == "1":
            id_filtro_estacion = request.POST.get('estacion')
            page_number = int(request.POST.get('pagina', '1'))

            if id_filtro_estacion:
                reportes = Reportes.objects.filter(id_medicion__id_estacion=id_filtro_estacion).order_by('id')
        else:
            mensaje = "Error en la solicitud POST"

    paginator = Paginator(reportes, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        'reportes' : reportes,
        'estaciones' : estaciones,
        'pagina_reportes' : page_obj, 
        'mensaje' : page_obj,
    }
    template = loader.get_template('index_reportes.html')
    return HttpResponse(template.render(context, request))
