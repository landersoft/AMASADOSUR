from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from abastecimiento.forms import ProductoForm
from .models import Producto,Proveedor


def index(request):
    return render(request, 'ventas/menu2.html')


class ProductoList(ListView):
    model = Producto
    paginate_by = 20
    template_name = 'abastecimiento/productos.html'

class ProductoCreate(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'abastecimiento/producto_add.html'
    success_url = reverse_lazy('abastecimiento:productos')





