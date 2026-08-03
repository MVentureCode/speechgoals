from django.urls import path
from . import views

# Cada 'path' conecta una URL con la función de views.py que la atiende.
# El parámetro 'name' permite referenciar la URL desde los templates

urlpatterns = [
    # Ruta raíz del sitio: muestra directamente el catálogo de objetivos
    # (reutiliza la misma vista que 'objetivos/', evita un 404 al entrar al dominio)
    path('', views.lista_objetivos, name='inicio'),

    # --- Rutas de apoyo: Paciente ---
    # No están enlazadas desde el menú principal, pero permiten consultar
    # pacientes de prueba y sus objetivos recomendados de forma manual.
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),

    # --- Rutas del modelo principal de la entrega: Objetivo ---
    # <int:objetivo_id> captura el id del objetivo desde la URL y lo pasa
    # como argumento a la vista detalle_objetivo
    path('objetivos/', views.lista_objetivos, name='lista_objetivos'),
    path('objetivos/<int:objetivo_id>/', views.detalle_objetivo, name='detalle_objetivo'),
]