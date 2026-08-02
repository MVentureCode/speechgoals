from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelos según el diagrama de clases: Diagnostico, Paciente, Objetivo, PlanTratamiento.
# Nota: Paciente no guarda datos identificativos (nombre, contacto, etc.),
# solo edad y diagnóstico, para evitar manejar datos sensibles en esta actividad.


# AREA_CHOICES se define fuera de las clases porque la reutilizan tanto
# Diagnostico como Objetivo: el área del diagnóstico del paciente es el
# criterio que se cruza con el área de cada objetivo para recomendarlo.
AREA_CHOICES = [
    ('habla', 'Habla'),
    ('lenguaje', 'Lenguaje'),
    ('comunicacion', 'Comunicación'),
    ('deglucion', 'Deglución'),
]


class Diagnostico(models.Model):
    """Catálogo de diagnósticos logopédicos (Dislalia, TDL, Disfemia, etc.),
    cada uno asociado a un área de trabajo principal."""
    nombre = models.CharField(max_length=200, help_text="Ej: Dislalia, TDL, Disfemia, Afasia, TEA, Síndrome genético...")
    area_afectada = models.CharField(max_length=20, choices=AREA_CHOICES)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        # get_area_afectada_display() devuelve el texto legible del choice
        # (ej. "Habla") en lugar del valor guardado en la base de datos (ej. "habla")
        return f"{self.nombre} ({self.get_area_afectada_display()})"


class Paciente(models.Model):
    """Representa un caso clínico anonimizado: solo edad y diagnóstico,
    sin ningún dato identificativo del paciente real."""

    # MaxValueValidator limita a 120 porque no tiene sentido clínico una edad mayor;
    # MinValueValidator(0) es redundante con PositiveSmallIntegerField, pero se
    # deja explícito para que el rango quede claro a simple vista
    edad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='pacientes')

    def __str__(self):
        return f"Paciente {self.id} ({self.edad} años) - {self.diagnostico.nombre}"

    def objetivos_recomendados(self):
        """Devuelve los objetivos cuya área coincide con el diagnóstico
        y cuyo rango de edad incluye la edad del paciente.
        __lte = menor o igual que / __gte = mayor o igual que"""
        return Objetivo.objects.filter(
            area=self.diagnostico.area_afectada,
            edad_minima__lte=self.edad,
            edad_maxima__gte=self.edad,
        )


class Objetivo(models.Model):
    """Catálogo de objetivos de tratamiento. El rango de edad
    (edad_minima - edad_maxima) determina si un objetivo es apto
    para un paciente concreto; es el modelo principal de la entrega."""

    DIFICULTAD_CHOICES = [
        (1, 'Baja'),
        (2, 'Media'),
        (3, 'Alta'),
    ]

    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    descripcion = models.CharField(max_length=200)
    dificultad = models.PositiveSmallIntegerField(choices=DIFICULTAD_CHOICES, default=1)
    edad_minima = models.PositiveSmallIntegerField(default=0)
    edad_maxima = models.PositiveSmallIntegerField(default=99)

    def __str__(self):
        return f"{self.descripcion} [{self.get_area_display()}, dificultad {self.dificultad}]"

    class Meta:
        # Orden por defecto del listado: agrupado por área y luego por dificultad
        ordering = ['area', 'dificultad']


class PlanTratamiento(models.Model):
    """Vincula un paciente con los objetivos seleccionados para su tratamiento.
    Relación ManyToMany porque un plan puede incluir varios objetivos,
    y un mismo objetivo puede formar parte de varios planes."""

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='planes')
    objetivos = models.ManyToManyField(Objetivo, related_name='planes')
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Plan #{self.id} - Paciente {self.paciente_id}"