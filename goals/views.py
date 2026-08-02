from django.shortcuts import render, get_object_or_404
from .models import Paciente, Objetivo, Diagnostico, AREA_CHOICES


def lista_pacientes(request):
    """Muestra el listado de todos los pacientes registrados."""
    pacientes = Paciente.objects.all()
    return render(request, 'goals/lista_pacientes.html', {'pacientes': pacientes})


def detalle_paciente(request, paciente_id):
    """Muestra los datos de un paciente concreto junto con
    sus objetivos recomendados según edad y área afectada."""
    paciente = get_object_or_404(Paciente, id=paciente_id)
    objetivos = paciente.objetivos_recomendados()
    contexto = {'paciente': paciente, 'objetivos': objetivos}
    return render(request, 'goals/detalle_paciente.html', contexto)


def lista_objetivos(request):
    """Vista de listado (modelo principal de la entrega).
    Muestra el catálogo de objetivos, con opción de filtrar por área
    mediante un parámetro GET (ej: /objetivos/?area=habla)."""
    area_seleccionada = request.GET.get('area')

    if area_seleccionada:
        objetivos = Objetivo.objects.filter(area=area_seleccionada)
    else:
        objetivos = Objetivo.objects.all()

    contexto = {
        'objetivos': objetivos,
        'areas': AREA_CHOICES,
        'area_seleccionada': area_seleccionada,
    }
    return render(request, 'goals/lista_objetivos.html', contexto)


def detalle_objetivo(request, objetivo_id):
    """Vista de detalle (modelo principal de la entrega).
    Muestra la información completa de un objetivo concreto."""
    objetivo = get_object_or_404(Objetivo, id=objetivo_id)
    return render(request, 'goals/detalle_objetivo.html', {'objetivo': objetivo})