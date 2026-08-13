from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator

from .models import Paciente, Objetivo, Diagnostico, AREA_CHOICES
from .forms import ObjetivoForm


# =========================================================
# PACIENTES
# =========================================================

def lista_pacientes(request):
    """
    Muestra el listado de todos los pacientes registrados.
    """
    pacientes = Paciente.objects.all()
    return render(
        request,
        'goals/lista_pacientes.html',
        {'pacientes': pacientes}
    )


def detalle_paciente(request, paciente_id):
    """
    Muestra los datos de un paciente concreto junto con
    sus objetivos recomendados según edad y área afectada.
    """
    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )
    objetivos = paciente.objetivos_recomendados()

    contexto = {
        'paciente': paciente,
        'objetivos': objetivos
    }

    return render(
        request,
        'goals/detalle_paciente.html',
        contexto
    )


# =========================================================
# OBJETIVOS
# =========================================================

def lista_objetivos(request):
    """Muestra el catálogo de objetivos con búsqueda, filtros y ordenación."""
    busqueda = request.GET.get('q')
    area_seleccionada = request.GET.get('area')
    edad_seleccionada = request.GET.get('edad')

    objetivos = Objetivo.objects.all()

    if busqueda:
        objetivos = objetivos.filter(
            descripcion__icontains=busqueda
        )

    if area_seleccionada:
        objetivos = objetivos.filter(
            area=area_seleccionada
        )

    if edad_seleccionada:
        objetivos = objetivos.filter(
            edad_minima__lte=edad_seleccionada,
            edad_maxima__gte=edad_seleccionada,
        )

    orden = request.GET.get('order', 'area')
    direccion = request.GET.get('dir', 'asc')

    ordenes_permitidos = {
        'descripcion': 'descripcion',
        'area': 'area',
        'dificultad': 'dificultad',
        'edad_minima': 'edad_minima',
        'edad_maxima': 'edad_maxima',
    }

    campo_orden = ordenes_permitidos.get(orden, 'area')

    if direccion == 'desc':
        campo_orden = '-' + campo_orden

    objetivos = objetivos.order_by(campo_orden)

    paginador = Paginator(objetivos, 10)
    numero_pagina = request.GET.get('page', 1)
    pagina_objetivos = paginador.get_page(numero_pagina)

    contexto = {
        'objetivos': pagina_objetivos,
        'areas': AREA_CHOICES,
        'area_seleccionada': area_seleccionada,
        'edad_seleccionada': edad_seleccionada,
        'busqueda': busqueda,
        'orden': orden,
        'direccion': direccion,
    }

    return render(
        request,
        'goals/lista_objetivos.html',
        contexto
    )


def detalle_objetivo(request, objetivo_id):
    """Muestra el detalle de un objetivo concreto."""
    objetivo = get_object_or_404(
        Objetivo,
        id=objetivo_id
    )
    return render(
        request,
        'goals/detalle_objetivo.html',
        {'objetivo': objetivo}
    )


# =========================================================
# CREAR OBJETIVO
# =========================================================

@login_required
def crear_objetivo(request):
    """Permite crear un nuevo objetivo terapéutico."""
    if request.method == 'POST':
        form = ObjetivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'El objetivo se ha creado correctamente.'
            )
            return redirect('goals:lista_objetivos')
    else:
        form = ObjetivoForm()

    return render(
        request,
        'goals/objetivo_form.html',
        {
            'form': form,
            'titulo': 'Crear objetivo'
        }
    )


# =========================================================
# EDITAR OBJETIVO
# =========================================================

@login_required
def editar_objetivo(request, objetivo_id):
    """Permite editar un objetivo existente."""
    objetivo = get_object_or_404(
        Objetivo,
        id=objetivo_id
    )

    if request.method == 'POST':
        form = ObjetivoForm(
            request.POST,
            instance=objetivo
        )
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'El objetivo se ha actualizado correctamente.'
            )
            return redirect(
                'goals:detalle_objetivo',
                objetivo_id=objetivo.id
            )
    else:
        form = ObjetivoForm(
            instance=objetivo
        )

    return render(
        request,
        'goals/objetivo_form.html',
        {
            'form': form,
            'titulo': 'Editar objetivo'
        }
    )


# =========================================================
# ELIMINAR OBJETIVO
# =========================================================

@login_required
def eliminar_objetivo(request, objetivo_id):
    """Permite eliminar un objetivo existente."""
    objetivo = get_object_or_404(Objetivo, id=objetivo_id)

    if request.method == 'POST':
        objetivo.delete()
        messages.success(
            request,
            'El objetivo se ha eliminado correctamente.'
        )
        return redirect('goals:lista_objetivos')

    return render(
        request,
        'goals/eliminar_objetivo.html',
        {'objetivo': objetivo}
    )


# =========================================================
# REGISTRO DE USUARIOS
# =========================================================

def registro(request):
    """Permite que un usuario cree una cuenta."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Tu cuenta se ha creado correctamente. Ya puedes iniciar sesión.'
            )
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(
        request,
        'registration/register.html',
        {'form': form}
    )