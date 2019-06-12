from django.shortcuts import render
from django.views.generic import ListView

from .models import Producto,Proveedor


def index(request):
    return render(request, 'ventas/menu2.html')


class ProductoList(ListView):
    model = Producto
    template_name='abastecimiento/productos.html'



