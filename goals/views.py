from django.shortcuts import render, get_object_or_404
from .models import Paciente, Objetivo, Diagnostico, AREA_CHOICES
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def lista_pacientes(request):
    """Muestra el listado de todos los pacientes registrados.
    No forma parte del flujo principal de la entrega,
    pero se conserva para poder consultar pacientes de prueba."""
    pacientes = Paciente.objects.all()
    return render(request, 'goals/lista_pacientes.html', {'pacientes': pacientes})


def detalle_paciente(request, paciente_id):
    """Muestra los datos de un paciente concreto junto con
    sus objetivos recomendados según edad y área afectada.
    Demuestra la lógica de recomendación automática definida en el modelo Paciente (objetivos_recomendados)."""

    # get_object_or_404 busca el paciente por su id;
    # si no existe, devuelve automáticamente un error 404 en vez de crashear
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Llamamos al método definido en el modelo Paciente, que ya contiene
    # la lógica de filtrado por área de diagnóstico y rango de edad
    objetivos = paciente.objetivos_recomendados()

    contexto = {'paciente': paciente, 'objetivos': objetivos}
    return render(request, 'goals/detalle_paciente.html', contexto)


def lista_objetivos(request):
    """Vista de listado (modelo principal de la entrega).
    Muestra el catálogo de objetivos, permitiendo filtrar por área y/o
    por edad mediante parámetros GET (ej: /objetivos/?area=habla&edad=5)."""

    # request.GET.get(...) lee los parámetros enviados por el formulario
    # de filtro; devuelve None si el usuario no seleccionó nada
    area_seleccionada = request.GET.get('area')
    edad_seleccionada = request.GET.get('edad')

    # Partimos del catálogo completo y aplicamos los filtros solo
    # si el usuario los indicó, para no restringir de más por defecto
    objetivos = Objetivo.objects.all()

    if area_seleccionada:
        objetivos = objetivos.filter(area=area_seleccionada)

    if edad_seleccionada:
        # Buscamos objetivos cuyo rango de edad incluya la edad indicada:
        # edad_minima <= edad_seleccionada <= edad_maxima
        # __lte = menor o igual que / __gte = mayor o igual que
        objetivos = objetivos.filter(
            edad_minima__lte=edad_seleccionada,
            edad_maxima__gte=edad_seleccionada,
        )

    # Pasamos también las áreas disponibles y los valores seleccionados,
    # para que el template pueda dibujar el formulario y recordar la selección
    contexto = {
        'objetivos': objetivos,
        'areas': AREA_CHOICES,
        'area_seleccionada': area_seleccionada,
        'edad_seleccionada': edad_seleccionada,
    }
    return render(request, 'goals/lista_objetivos.html', contexto)


def detalle_objetivo(request, objetivo_id):
    """Vista de detalle (modelo principal de la entrega).
    Muestra la información completa de un objetivo concreto."""

    # Si el id no corresponde a ningún objetivo existente,
    # Django devuelve automáticamente una página de error 404
    objetivo = get_object_or_404(Objetivo, id=objetivo_id)
    return render(request, 'goals/detalle_objetivo.html', {'objetivo': objetivo})


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
        {'form': form, 'titulo': 'Crear objetivo'}
    )


@login_required
def editar_objetivo(request, objetivo_id):
    """Permite editar un objetivo existente."""
    objetivo = get_object_or_404(Objetivo, id=objetivo_id)

    if request.method == 'POST':
        form = ObjetivoForm(request.POST, instance=objetivo)

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
        form = ObjetivoForm(instance=objetivo)

    return render(
        request,
        'goals/objetivo_form.html',
        {
            'form': form,
            'titulo': 'Editar objetivo'
        }
    )
