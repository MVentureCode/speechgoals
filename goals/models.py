from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Creo clses según el diagrama de clases: Diagnostico, Paciente, Objetivo, PlanTratamiento


AREA_CHOICES = [
    ('habla', 'Habla'),
    ('lenguaje', 'Lenguaje'),
    ('comunicacion', 'Comunicación'),
    ('deglucion', 'Deglución'),
]


class Diagnostico(models.Model):
    nombre = models.CharField(max_length=200, help_text="Ej: Dislalia, TDL, Disfemia, Afasia, TEA, Síndrome genético...")
    area_afectada = models.CharField(max_length=20, choices=AREA_CHOICES)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_area_afectada_display()})"


# MaxValueValidator limita a 120 porque no tiene sentido clínico una edad mayor
class Paciente(models.Model):
    edad = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)]
    )
    diagnostico = models.ForeignKey(Diagnostico, on_delete=models.CASCADE, related_name='pacientes')

    def __str__(self):
        return f"Paciente {self.id} ({self.edad} años) - {self.diagnostico.nombre}"

    def objetivos_recomendados(self):
        """Devuelve los objetivos cuya área coincide con el diagnóstico
        y cuyo rango de edad incluye la edad del paciente."""
        return Objetivo.objects.filter(
            area=self.diagnostico.area_afectada,
            edad_minima__lte=self.edad,
            edad_maxima__gte=self.edad,
        )

# El rango de edad del objetivo determina si es apto para el paciente
class Objetivo(models.Model):
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
        ordering = ['area', 'dificultad']


class PlanTratamiento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='planes')
    objetivos = models.ManyToManyField(Objetivo, related_name='planes')
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Plan #{self.id} - Paciente {self.paciente_id}"