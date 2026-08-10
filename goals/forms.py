from django import forms
from .models import Objetivo


class ObjetivoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Objetivo.

    ModelForm permite que Django genere automáticamente
    los campos del formulario a partir de nuestro modelo.
    """

    class Meta:
        # Indicamos qué modelo utiliza este formulario.
        model = Objetivo

        # Indicamos los campos que el usuario podrá completar
        # o modificar desde el formulario.
        fields = [
            'area',
            'descripcion',
            'dificultad',
            'edad_minima',
            'edad_maxima',
        ]

    def clean_descripcion(self):
        """
        Validación personalizada para la descripción.

        Django ejecuta este método automáticamente cuando
        valida el formulario.
        """

        # Recuperamos el valor introducido por el usuario.
        descripcion = self.cleaned_data.get('descripcion')

        # Comprobamos que no esté vacío ni contenga
        # únicamente espacios.
        if not descripcion or not descripcion.strip():
            raise forms.ValidationError(
                'La descripción del objetivo es obligatoria.'
            )

        # Devolvemos el texto limpio, eliminando espacios
        # innecesarios al principio y al final.
        return descripcion.strip()

    def clean(self):
        """
        Validación general del formulario.

        Aquí podemos comprobar relaciones entre varios campos,
        en este caso edad mínima y edad máxima.
        """

        # Primero ejecutamos las validaciones normales de Django.
        cleaned_data = super().clean()

        # Recuperamos las edades ya validadas.
        edad_minima = cleaned_data.get('edad_minima')
        edad_maxima = cleaned_data.get('edad_maxima')

        # Comprobamos que el rango de edad sea coherente.
        # Ejemplo válido: 3 - 8
        # Ejemplo incorrecto: 10 - 5
        if (
            edad_minima is not None
            and edad_maxima is not None
            and edad_minima > edad_maxima
        ):
            raise forms.ValidationError(
                'La edad mínima no puede ser mayor que la edad máxima.'
            )

        # Devolvemos los datos después de realizar las validaciones.
        return cleaned_data