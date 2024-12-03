from django.shortcuts import render, redirect
from .models import *

from django.contrib.auth.decorators import login_required
from .decorators import admin_required

@admin_required
def parametros(request):
    # Obtener los parámetros con la regla específica
    parametros = ParametrosMedicion.objects.filter(id_regla=1)
    valores = ParametrosMedicion.objects.all().values()
    reglas = ReglasMedicion.objects.all().values()
    
    mensaje = ""

    tipo_regla = request.GET.get('regla', '')

    if tipo_regla:
        valores_regla = ParametrosMedicion.objects.filter(id_regla=tipo_regla)
    else:
        valores_regla = []

    if request.method == "POST":

        tipo_formulario = request.POST.get('id_formulario', None)
        tipos = ["min", "ide", "max"]
        resultado = []
        
        if tipo_formulario == "1":

            valor_id_regla = request.POST.get('id_regla')
            parametros = ParametrosMedicion.objects.filter(id_regla=valor_id_regla)

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
        elif tipo_formulario == "2":
            nuevo_nombre = request.POST.get('nombre_regla')
            nueva_regla = ReglasMedicion(nombre=nuevo_nombre)
            nueva_regla.save()

            for id_medicion in range(1,9):
                obj_tipo_medicion = TiposMedicion.objects.get(id=id_medicion)
                nuevo_parametro = ParametrosMedicion(
                    id_regla = nueva_regla,
                    id_tipo_medicion = obj_tipo_medicion,
                    valor_min= request.POST.get(f'v_min_{str(id_medicion)}'),
                    valor_ide= request.POST.get(f'v_ide_{str(id_medicion)}'),
                    valor_max= request.POST.get(f'v_max_{str(id_medicion)}')
                )
                nuevo_parametro.save()
            
            mensaje = "Regla creada exitosamente"
        elif tipo_formulario == "3":
            id_regla_eliminar = request.POST.get('id_regla_eliminar')
            try:
                ParametrosMedicion.objects.filter(id_regla=id_regla_eliminar).delete()
                regla = ReglasMedicion.objects.get(id=id_regla_eliminar)
                regla.delete()
                
                mensaje = "Regla y parámetros eliminados exitosamente"
            except ReglasMedicion.DoesNotExist:
                mensaje = "La regla con el ID especificado no existe"
        else:
            mensaje = "Error en solicitud POST"

    # Contexto para el template
    context = {
        'parametros': parametros,
        'reglas': reglas,
        'mensaje': mensaje,
        'valores_regla': valores_regla,
    }

    return render(request, 'index_parametros.html', context)


