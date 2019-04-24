from django import forms
from .models import Cliente 



class RegCliente(forms.Form):
     rut = forms.IntegerField()
     nombre = forms.CharField(max_length=100)
     direccion = forms.CharField(max_length=100)
