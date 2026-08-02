from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_objetivos, name='inicio'),  # la raíz muestra el catálogo directamente
    path('pacientes/', views.lista_pacientes, name='lista_pacientes'),
    path('pacientes/<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    # Rutas del modelo principal: Objetivos
    path('objetivos/', views.lista_objetivos, name='lista_objetivos'),
    path('objetivos/<int:objetivo_id>/', views.detalle_objetivo, name='detalle_objetivo'),
]
