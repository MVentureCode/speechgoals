from django.urls import path
from . import views

# Nombre de la aplicación.
# Permite utilizar espacios de nombres en las URLs desde los templates.
# Por ejemplo: {% url 'goals:lista_objetivos' %}
app_name = 'goals'

# Cada 'path' conecta una URL con la función de views.py que la atiende.
# El parámetro 'name' permite referenciar la URL desde los templates.

urlpatterns = [
    # Ruta raíz del sitio: muestra directamente el catálogo de objetivos.
    # Reutiliza la misma vista que 'objetivos/' para evitar un 404 al entrar directamente al dominio.
    path('', views.lista_objetivos, name='inicio'),

    # --- Rutas de apoyo: Paciente ---
    # No están enlazadas desde el menú principal, pero permiten consultar
    # pacientes de prueba y sus objetivos recomendados de forma manual.
    path(
        'pacientes/',
        views.lista_pacientes,
        name='lista_pacientes'
    ),
    path(
        'pacientes/<int:paciente_id>/',
        views.detalle_paciente,
        name='detalle_paciente'
    ),

    # --- Rutas del modelo principal de la entrega: Objetivo ---
    # Muestra el listado público de objetivos.
    path(
        'objetivos/',
        views.lista_objetivos,
        name='lista_objetivos'
    ),

    # Muestra el detalle de un objetivo concreto.
    # <int:objetivo_id> captura el ID desde la URL.
    path(
        'objetivos/<int:objetivo_id>/',
        views.detalle_objetivo,
        name='detalle_objetivo'
    ),

    # --- Rutas para crear y editar objetivos ---
    # Estas acciones requieren que el usuario haya iniciado sesión.
    # La protección se realiza en views.py mediante @login_required.

    # Permite crear un nuevo objetivo terapéutico.
    path(
        'objetivos/crear/',
        views.crear_objetivo,
        name='crear_objetivo'
    ),

    # Permite editar un objetivo existente.
    # <int:objetivo_id> indica qué objetivo queremos modificar.
    # Ejemplo: /objetivos/editar/5/
    path(
        'objetivos/editar/<int:objetivo_id>/',
        views.editar_objetivo,
        name='editar_objetivo'
    ),

    # --- Registro de usuarios ---
    # Permite que un usuario cree una cuenta nueva.
    path(
        'registro/',
        views.registro,
        name='registro'
    ),
]