from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import *
from .decorators import admin_required

@admin_required
def reportes(request):
    template = loader.get_template('index_reportes.html')
    reportes = Reportes.objects.all().order_by('id')[:5]
    context = {
        'reportes' : reportes,
    }
    return HttpResponse(template.render(context, request))
