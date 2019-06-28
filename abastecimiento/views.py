from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.forms import modelformset_factory
from django.urls import reverse_lazy

from .models import Producto,Proveedor,Compra,DetalleCompra
from django.forms import formsets, formset_factory
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'ventas/menu2.html')





class ProductoList(ListView):
    model = Producto
    paginate_by = 20
    template_name = 'abastecimiento/productos.html'





class CrearCompra(CreateView):
    pass


    


class ListadoCompras(ListView):
    model = Compra
    template_name = 'abastecimiento/compras.html'
    context_object_name = 'compras'


@login_required
def compra(request):
    return render(request, "abastecimiento/compra.html")


def nueva_compra(request):
    if request.method=="POST":
        rut_proveedor = request.POST['rut']
        print(rut_proveedor)
        try:
            proveedor = Proveedor.objects.get(rut=rut_proveedor)
            print(proveedor.nombre)
            
            context={
                'nombre': proveedor.nombre,
                'rut': proveedor.rut 
            }
            return render(request, 'abastecimiento/compra.html', context)
        except Proveedor.DoesNotExist:
            proveedor=None
            mesj = "Proveedor NO existe \n Redirigiendo"
            context={
                'mesj': mesj
            }
            return render(request,'ventas/info.html',context)


