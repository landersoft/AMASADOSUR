from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .models import Venta, Producto, DetalleVenta, Boleta, Factura, Cliente
from django.views.generic import ListView
from django.db.models import Q,F
from django.db.models import Sum, IntegerField
from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.
# @login_required
# def index(request):
#     return HttpResponse("Hola, mundo")

#1 Menu principal
@login_required 
def index(request):
    return render(request, 'ventas/menu.html')
#2 muestra boleta o factura
@login_required
def nueva2(request):
    return render(request, 'ventas/nueva.html')

@login_required
def nueva(request):
    #if request.method == 'POST':
        nueva_venta = Venta(usuario=request.user)
        nueva_venta.save()
        codigo_venta = Venta.objects.latest('id')
        print(codigo_venta)
        return render(request, 'ventas/venta.html')


    #return render(request, 'ventas/factura.html')

#3 eligió boleta 
@login_required
def boleta(request):

    if request.method == 'POST':
        nueva_venta = Venta(usuario=request.user)
        nueva_venta.save()
        codigo_venta = Venta.objects.latest('id')
        print(codigo_venta)
    return render(request, 'ventas/venta.html')
    
def detalleadd(request):
    if request.method == 'POST':        
        
        #de_venta = Venta.objects.latest('id')
        de_venta = Venta.objects.last()
        flotante = (request.POST['textinput'])
        de_producto = Producto.objects.get(pk = request.POST['textinput'])

        print(de_venta.id)
        print(de_producto.id)      
        #consulta para saber si hay mas de este mismo producto
        obj = DetalleVenta.objects.filter(id_producto = de_producto.id, id_venta=de_venta.id).first()
        
        #query = DetalleVenta.objects.filter(id_producto = flotante, id_venta = de_venta).count()
        precio = Producto.objects.get(id=flotante).precio_actual
        
        if obj is None:
            det_venta = DetalleVenta()
            det_venta.id_producto=de_producto
            det_venta.id_venta=de_venta
            det_venta.cantidad = 1 
            det_venta.precio_venta = precio
            det_venta.save()
        else:
            det_venta = DetalleVenta.objects.get(id_producto=de_producto, id_venta=de_venta)
            det_venta.cantidad += 1
            det_venta.save()

        
        print(de_producto.nombre)
        print(precio)
        print(det_venta.cantidad)
        print((det_venta.cantidad * det_venta.precio_venta))        
        total2 = DetalleVenta.objects.filter(id_venta=Venta.objects.latest('id')).aggregate(suma=Sum(F('precio_venta')*F('cantidad')))
        print("total consulta")
        de_venta.total = total2["suma"]
        print (total2["suma"])
        contador = len(total2)
        de_venta.save()
        

        subtotal= Venta.objects.last()
        return HttpResponseRedirect('lista/')


def boletaofactura(request):
        if request.method == 'POST':
                tipodocumento = request.POST['documento']
                if tipodocumento == 'boleta':
                        nueva_boleta = Boleta(id_venta=Venta.objects.latest('id'))


def formapago(request):
    if request.method == 'POST':
        forma = request.POST['exampleRadios']
        de_venta = Venta.objects.last()
        if forma =='option1':               
                de_venta.forma_pago='Efectivo'
                #nueva_boleta = Boleta(id_venta=Venta.objects.latest('id'))
        else:
                de_venta.forma_pago='Tarjeta'

        de_venta.save()
        return render(request, 'ventas/boletaofactura.html')

def tipodocumento(request):
        if request.method == 'POST':
                tipo = request.POST['documento']
                if tipo == 'boleta':
                        nueva_boleta = Boleta(id_venta=Venta.objects.latest('id'))
                        nueva_boleta.save()
                        return render(request, 'ventas/menu.html')
                else:
                        return render(request, 'ventas/verifica.html')

def guardarfactura(request):
    if request.method == 'POST':
        nueva_factura = Factura(id_venta=Venta.objects.latest('id'), id_cliente=(request.POST['textinput']) )
        nueva_factura.save()

class VentaList(ListView):

    model = DetalleVenta
    context_object_name = 'venta_list'

    def get_queryset(self):
        return DetalleVenta.objects.filter(id_venta=Venta.objects.latest('id'))
        #template_name = 'ventas/VentaList.html'
    
    def get_context_data(self, **kwargs):
        context = super(VentaList, self).get_context_data(**kwargs)
        context['suma'] = DetalleVenta.objects.filter(id_venta=Venta.objects.latest('id')).aggregate(total=Sum(F('precio_venta')*F('cantidad')))['total']
        print(context)
        return context

@login_required    
def pagar(request):
    if request.method == 'POST':
        costo = request.POST['suma']
        print (costo)
        return render( request, 'ventas/pagar.html', {'total': costo} )


def verifica(request):
        if request.method == 'POST':
                rut = request.POST['rut']
                cliente = Cliente.objects.filter(rut=rut)                
                print (cliente.exists())
                return render(request,'ventas/factura2.html',{ 'cliente':cliente })
                
#https://es.stackoverflow.com/questions/95569/recuperar-objectos-de-un-modelo-en-django


