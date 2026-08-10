from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import Paciente, Objetivo, Diagnostico, AREA_CHOICES
from .forms import ObjetivoForm


# =========================================================
# PACIENTES
# =========================================================

def lista_pacientes(request):
    """
    Muestra el listado de todos los pacientes registrados.

    No forma parte del flujo principal de la entrega,
    pero se conserva para poder consultar pacientes de prueba.
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

    # get_object_or_404 busca el paciente por su id.
    # Si no existe, devuelve automáticamente un error 404
    # en vez de producir un error en la aplicación.
    paciente = get_object_or_404(
        Paciente,
        id=paciente_id
    )

    # Llamamos al método definido en el modelo Paciente.
    # Este método contiene la lógica que busca objetivos
    # compatibles con el diagnóstico y la edad.
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
    """
    Muestra el catálogo de objetivos.

    Permite:
    - buscar por texto
    - filtrar por área
    - filtrar por edad
    - ordenar los resultados
    """

    # =====================================================
    # 1. RECUPERAR LOS PARÁMETROS DE LA URL
    # =====================================================

    # request.GET.get() lee los parámetros enviados
    # mediante la URL.

    # Ejemplo:
    # /objetivos/?q=lenguaje&area=habla&edad=5

    busqueda = request.GET.get('q')
    area_seleccionada = request.GET.get('area')
    edad_seleccionada = request.GET.get('edad')


    # =====================================================
    # 2. OBTENER TODOS LOS OBJETIVOS
    # =====================================================

    # Comenzamos con todos los objetivos de la base de datos.
    objetivos = Objetivo.objects.all()


    # =====================================================
    # 3. BÚSQUEDA POR TEXTO
    # =====================================================

    # Si el usuario ha escrito algo en el buscador,
    # buscamos ese texto dentro de la descripción.

    # __icontains significa:
    # "contiene este texto sin distinguir mayúsculas/minúsculas".

    if busqueda:
        objetivos = objetivos.filter(
            descripcion__icontains=busqueda
        )


    # =====================================================
    # 4. FILTRO POR ÁREA
    # =====================================================

    # Si el usuario seleccionó un área,
    # mostramos solamente los objetivos de esa área.

    if area_seleccionada:
        objetivos = objetivos.filter(
            area=area_seleccionada
        )


    # =====================================================
    # 5. FILTRO POR EDAD
    # =====================================================

    # Si el usuario introdujo una edad,
    # buscamos objetivos cuyo rango de edad incluya
    # la edad indicada.

    # Ejemplo:
    # edad = 5
    #
    # edad_minima <= 5
    # edad_maxima >= 5

    if edad_seleccionada:
        objetivos = objetivos.filter(
            edad_minima__lte=edad_seleccionada,
            edad_maxima__gte=edad_seleccionada,
        )


    # =====================================================
    # 6. ORDENACIÓN
    # =====================================================

    # Recuperamos de la URL el campo por el que
    # queremos ordenar.

    # Ejemplo:
    # ?order=dificultad

    # Si no se indica ningún campo,
    # utilizamos 'area' como orden por defecto.

    orden = request.GET.get(
        'order',
        'area'
    )


    # Recuperamos la dirección del orden.

    # asc  = ascendente
    # desc = descendente

    # Si no se indica ninguna dirección,
    # utilizamos ascendente.

    direccion = request.GET.get(
        'dir',
        'asc'
    )


    # =====================================================
    # 7. CAMPOS PERMITIDOS PARA ORDENAR
    # =====================================================

    # Creamos un diccionario con los únicos campos
    # que permitimos utilizar para ordenar.

    # La clave es el valor que recibimos desde la URL.
    # El valor es el nombre real del campo del modelo.

    ordenes_permitidos = {
        'descripcion': 'descripcion',
        'area': 'area',
        'dificultad': 'dificultad',
        'edad_minima': 'edad_minima',
        'edad_maxima': 'edad_maxima',
    }


    # Comprobamos si el campo recibido está permitido.

    # Si no está permitido, utilizamos 'area'
    # como orden por defecto.

    campo_orden = ordenes_permitidos.get(
        orden,
        'area'
    )


    # =====================================================
    # 8. DIRECCIÓN DEL ORDEN
    # =====================================================

    # Django utiliza '-' delante del nombre del campo
    # para indicar orden descendente.

    # Ejemplo:
    # dificultad   → ascendente
    # -dificultad  → descendente

    if direccion == 'desc':
        campo_orden = '-' + campo_orden


    # Aplicamos finalmente la ordenación.

    objetivos = objetivos.order_by(
        campo_orden
    )


    # =====================================================
    # 9. CONTEXTO PARA EL TEMPLATE
    # =====================================================

    # Enviamos al HTML:
    #
    # - los objetivos encontrados
    # - las áreas disponibles
    # - los filtros seleccionados
    # - la búsqueda realizada
    # - el orden seleccionado
    # - la dirección seleccionada

    contexto = {
        'objetivos': objetivos,
        'areas': AREA_CHOICES,
        'area_seleccionada': area_seleccionada,
        'edad_seleccionada': edad_seleccionada,
        'busqueda': busqueda,
        'orden': orden,
        'direccion': direccion,
    }


    # Finalmente mostramos el template
    # lista_objetivos.html.

    return render(
        request,
        'goals/lista_objetivos.html',
        contexto
    )


def detalle_objetivo(request, objetivo_id):
    """
    Muestra el detalle de un objetivo concreto.
    """

    # Si el ID no corresponde a ningún objetivo existente,
    # Django devuelve automáticamente un error 404.
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
    """
    Permite crear un nuevo objetivo terapéutico.

    @login_required garantiza que solamente
    los usuarios autenticados puedan acceder.
    """

    # Comprobamos si el formulario ha sido enviado.
    if request.method == 'POST':

        # Creamos el formulario utilizando
        # los datos enviados por el usuario.
        form = ObjetivoForm(request.POST)

        # Comprobamos las validaciones del formulario.
        if form.is_valid():

            # Guardamos el nuevo objetivo.
            form.save()

            # Mostramos un mensaje de éxito.
            messages.success(
                request,
                'El objetivo se ha creado correctamente.'
            )

            # Volvemos al listado de objetivos.
            return redirect(
                'goals:lista_objetivos'
            )

    else:

        # Si todavía no se ha enviado el formulario,
        # mostramos un formulario vacío.
        form = ObjetivoForm()


    # Mostramos el formulario.
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
    """
    Permite editar un objetivo existente.

    Solo pueden acceder usuarios autenticados.
    """

    # Buscamos el objetivo que queremos editar.
    # Si no existe, mostramos un error 404.
    objetivo = get_object_or_404(
        Objetivo,
        id=objetivo_id
    )


    # Comprobamos si el formulario ha sido enviado.
    if request.method == 'POST':

        # instance=objetivo indica que queremos
        # modificar ese objetivo existente.
        form = ObjetivoForm(
            request.POST,
            instance=objetivo
        )

        # Comprobamos las validaciones.
        if form.is_valid():

            # Guardamos los cambios.
            form.save()

            # Mostramos mensaje de éxito.
            messages.success(
                request,
                'El objetivo se ha actualizado correctamente.'
            )

            # Volvemos al detalle del objetivo.
            return redirect(
                'goals:detalle_objetivo',
                objetivo_id=objetivo.id
            )

    else:

        # Si todavía no se ha enviado el formulario,
        # mostramos los datos actuales del objetivo.
        form = ObjetivoForm(
            instance=objetivo
        )


    # Mostramos el formulario de edición.
    return render(
        request,
        'goals/objetivo_form.html',
        {
            'form': form,
            'titulo': 'Editar objetivo'
        }
    )


# =========================================================
# REGISTRO DE USUARIOS
# =========================================================

def registro(request):
    """
    Permite que un usuario cree una cuenta.

    Utilizamos UserCreationForm, proporcionado por Django,
    para gestionar y validar el nombre de usuario
    y la contraseña.
    """

    # Comprobamos si el formulario ha sido enviado.
    if request.method == 'POST':

        # Recibimos los datos enviados por el usuario.
        form = UserCreationForm(
            request.POST
        )

        # Comprobamos si los datos cumplen
        # las validaciones de Django.
        if form.is_valid():

            # Guardamos el nuevo usuario en la base de datos.
            form.save()

            # Mostramos un mensaje de confirmación.
            messages.success(
                request,
                'Tu cuenta se ha creado correctamente. '
                'Ya puedes iniciar sesión.'
            )

            # Después del registro,
            # enviamos al usuario al login.
            return redirect('login')

    else:

        # Si el usuario acaba de entrar en la página,
        # mostramos un formulario vacío.
        form = UserCreationForm()


    # Mostramos el formulario de registro.
    return render(
        request,
        'registration/register.html',
        {'form': form}
    )