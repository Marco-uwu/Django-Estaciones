from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import admin_required

@admin_required
def inicio(request):
    estaciones = Estaciones.objects.all().values()[:5]
    parametros = ParametrosMedicion.objects.filter(id_regla=1)
    template = loader.get_template('inicio.html')
    context = {
        'estaciones' : estaciones,
        'parametros' : parametros,
    }
    return HttpResponse(template.render(context, request))


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if user_profile.user_type == 'admin':
        return redirect('inicio')
    elif user_profile.user_type == 'client':
        return render(request, 'client_dashboard.html')
    else:
        return redirect('/login/')
