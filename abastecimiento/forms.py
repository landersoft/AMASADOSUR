from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'precio_actual',
            'margen',

        ]
        labels ={
            'nombre': 'Nombre',
            'descripcion': 'Descripción',
            'precio_actual': 'Precio Actual',
            'margen': 'Margen',

        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'margen': forms.NumberInput(attrs={'class': 'form-control'}),
        }

