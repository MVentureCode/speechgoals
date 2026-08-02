from django.contrib import admin
from .models import Diagnostico, Paciente, Objetivo, PlanTratamiento


@admin.register(Diagnostico)  # Forma abreviada de registrar el modelo con esta clase
class DiagnosticoAdmin(admin.ModelAdmin):
    # Columnas que se muestran en el listado (evita tener que entrar a cada registro)
    list_display = ('nombre', 'area_afectada')

    # Añade un filtro lateral para ver solo los diagnósticos de un área concreta
    list_filter = ('area_afectada',)

    # Activa la barra de búsqueda arriba del listado (busca por nombre)
    search_fields = ('nombre',)


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'edad', 'diagnostico')

    # El doble guion bajo "__" permite filtrar por un campo de una tabla
    # relacionada (en este caso, el área del diagnóstico asociado al paciente)
    list_filter = ('diagnostico__area_afectada',)

    # Búsqueda a través de la relación ForeignKey (busca por nombre de diagnóstico)
    search_fields = ('diagnostico__nombre',)


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'area', 'dificultad', 'edad_minima', 'edad_maxima')

    # Filtros laterales por área y por nivel de dificultad
    list_filter = ('area', 'dificultad')

    search_fields = ('descripcion',)

    # Orden por defecto del listado: primero por área, luego por dificultad
    ordering = ('area', 'dificultad')


# Un plan agrupa varios objetivos (ManyToMany), así que usamos un widget
# especial para seleccionarlos más fácilmente.
@admin.register(PlanTratamiento)
class PlanTratamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'fecha_creacion')

    # filter_horizontal mejora la interfaz para campos ManyToMany:
    # muestra dos cajas (disponibles / seleccionados) en lugar de
    # un select múltiple difícil de manejar con muchos objetivos.
    filter_horizontal = ('objetivos',)

    # Filtro lateral por fecha de creación del plan
    list_filter = ('fecha_creacion',)
