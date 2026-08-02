from django.shortcuts import render, get_object_or_404
from .models import Paciente, Objetivo, Diagnostico


def lista_pacientes(request):
    """Muestra el listado de todos los pacientes registrados."""
    pacientes = Paciente.objects.all()
    return render(request, 'goals/lista_pacientes.html', {'pacientes': pacientes})


def detalle_paciente(request, paciente_id):
    """Muestra los datos de un paciente concreto junto con sus objetivos recomendados según edad y área afectada."""
    # get_object_or_404 busca el paciente por su id;
    # si no existe, devuelve automáticamente un error 404 en vez de crashear
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Usamos el método que ya definimos en el modelo Paciente
    objetivos = paciente.objetivos_recomendados()

    contexto = {
        'paciente': paciente,
        'objetivos': objetivos,
    }
    return render(request, 'goals/detalle_paciente.html', contexto)


def lista_objetivos(request):
    """Muestra el listado completo de objetivos disponibles, sin filtrar por paciente."""
    objetivos = Objetivo.objects.all()
    return render(request, 'goals/lista_objetivos.html', {'objetivos': objetivos})# Create your views here.
