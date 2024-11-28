from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@admin_required
def parametros(request):
    # Obtener los parámetros con la regla específica
    parametros = ParametrosMedicion.objects.filter(id_regla=1)
    mensaje = ""

    if request.method == "POST":
        tipos = ["min", "ide", "max"]
        resultado = []  # Guarda los valores ingresados para depuración o procesamiento

        for i in range(8):
            valores = []
            for tipo in tipos:
                nombre = f"v_{tipo}_{str(i+1)}"
                valor = request.POST.get(nombre, None)

                # Valida que el valor no sea None antes de agregarlo
                if valor is not None:
                    valores.append(valor)
                else:
                    valores.append("")  # Agregar un valor vacío si falta

            resultado.append(valores)  # Agregar al resultado completo

            # Asignar valores a los parámetros correspondientes
            if i < len(parametros):  # Evitar errores de índice si hay menos de 8 parámetros
                parametros[i].valor_min = valores[0]
                parametros[i].valor_ide = valores[1]
                parametros[i].valor_max = valores[2]
                parametros[i].save()  # Guarda los cambios en la base de datos

                # Construir el mensaje acumulativo
        mensaje = "Cambios guardados correctamente! :)"

    # Contexto para el template
    context = {
        'parametros': parametros,
        'mensaje': mensaje,
    }

    return render(request, 'index_parametros.html', context)

