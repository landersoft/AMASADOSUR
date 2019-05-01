from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from abastecimiento.models import DetalleCompra
from .models import Venta, Producto, DetalleVenta, Boleta, Factura, Cliente
from django.views.generic import ListView
from django.db.models import Q,F
from django.db.models import Sum, IntegerField
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import RegCliente


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
                        venta = Boleta.objects.latest('id').id_venta
                        print ("id de venta es " + str(venta))
                        #este te entrega el id producto y la cantidad a restar. 
                        detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad').count()
                        print("esto es el contador de objetos del queryset " + str(detalles))
                        
                        #este es para cargar todos los objetos de tipo detalleventa
                        
                        detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad')
                        print(detalles)
                        for detalle in detalles:
                        #instance.id_producto.stock += instance.cantidad
                                stock_actual=Producto.objects.get(id=detalle['id_producto']).stock
                                print(stock_actual)
                                #producto = Producto.objects.get(id=detalle['id_producto']).stock-=detalle['cantidad']
                                producto = Producto.objects.get(id=detalle['id_producto'])
                                producto.stock-=detalle['cantidad']
                                producto.save()
                        

###################################Como obtener el total de ventas################################################################                        

                        ventas=Boleta.objects.all().values('id_venta')
                        total=0
                        for venta in ventas:
                                sumando=Venta.objects.get(id=venta['id_venta']).total      
                                total = total + sumando
                        
                        print ('este es el total de venta: '+str(total))

                        return render(request, 'ventas/menu.html')
                else:
                        return render(request, 'ventas/verifica.html')

###################################################################################################################################

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
                try:
                        cliente = Cliente.objects.get(rut=request.POST['rut'])
                except Cliente.DoesNotExist:
                        cliente = None
                        return HttpResponseRedirect('registrocliente')


                print("este es el id del cliente " +str(cliente))
                                
                if cliente!=(Null or None):
                        nueva_factura2 = Factura(id_venta=Venta.objects.latest('id'), id_cliente=cliente)
                        nueva_factura2.save()

                        venta = Factura.objects.latest('id').id_venta
                        print ("id de venta es " + str(venta))
                        #este te entrega el id producto y la cantidad a restar. 
                        detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad').count()
                        print("esto es el contador de elementos del queryset " + str(detalles))
                        
                        #este es para cargar todos los objetos de tipo detalleventa
                        
                        detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad')
                        print(detalles)
                        for detalle in detalles:
                        #instance.id_producto.stock += instance.cantidad
                                stock_actual=Producto.objects.get(id=detalle['id_producto']).stock
                                print(stock_actual)
                                #producto = Producto.objects.get(id=detalle['id_producto']).stock-=detalle['cantidad']
                                producto = Producto.objects.get(id=detalle['id_producto'])
                                producto.stock-=detalle['cantidad']
                                producto.save()


                        return render(request, 'ventas/menu.html')
                else:
                        return HttpResponseRedirect('registrocliente')
                
#https://es.stackoverflow.com/questions/95569/recuperar-objectos-de-un-modelo-en-django

def registracliente(request):
        form = RegCliente(request.POST or None)
        context = {
                "form":form
                
        }
        if form.is_valid():
                form_data = form.cleaned_data
                dni = form_data.get("rut")
                name = form_data.get("nombre")
                adress = form_data.get("direccion")
                obj = Cliente.objects.create(rut=dni,nombre=name,direccion=adress)
                nueva_factura = Factura(id_venta=Venta.objects.latest('id'), id_cliente=Cliente.objects.get(rut=dni))
                nueva_factura.save()



                venta = Factura.objects.latest('id').id_venta
                print ("id de venta es " + str(venta))
                        #este te entrega el id producto y la cantidad a restar. 
                detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad').count()
                print("esto es el contador de elementos del queryset " + str(detalles))
                        
                        #este es para cargar todos los objetos de tipo detalleventa
                        
                detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad')
                print(detalles)
                for detalle in detalles:
                        #instance.id_producto.stock += instance.cantidad
                        stock_actual=Producto.objects.get(id=detalle['id_producto']).stock
                        print(stock_actual)
                                #producto = Producto.objects.get(id=detalle['id_producto']).stock-=detalle['cantidad']
                        producto = Producto.objects.get(id=detalle['id_producto'])
                        producto.stock-=detalle['cantidad']
                        producto.save()

                return render(request, 'ventas/menu.html')
                #este te entrega el id de venta
                
                

        return render(request, "ventas/registrocliente.html", context)


def margen(request):
    if request.method=='POST':
        ventas = Venta.objects.values('boleta__id','total').aggregate(suma=Sum('total'))
        costo = DetalleVenta.objects.values('id_venta_id','id_producto','cantidad')





#Entrega las ID de las ventas en boleta

#Total de todas las ventas
#Venta.objects.values('boleta__id','total').aggregate(suma=Sum('total'))
#Total de costo de las ventas
#DetalleVenta.objects.values('id_venta_id','id_producto','cantidad')

#Entrega la cantidad de productos vendidos
#DetalleVenta.objects.values('id_producto').order_by('id_producto').annotate(total=Sum('cantidad'))


#id_cantidad=DetalleVenta.objects.values('id_venta_id','id_producto','cantidad')
#suma=DetalleCompra.objects.filter(id_producto=id_cantidad.values('id_producto').values('precio_unitario'))


#suma=DetalleCompra.objects.filter(id_producto=id_cantidad.values('id_producto')).values('precio_unitario')

###################################################################
#1)Total boletas
#ventas = Boleta.objects.all()
#ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id_venta_id')))
#total = ven.annotate(Sum(F('precio_venta')*F('cantidad')))

#2)Cantidad de productos vendidos.
#ventas = Boleta.objects.all()
#ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id_venta_id')))
#cantidad=ven.values('id_producto_id').order_by('id_producto_id').annotate(total=Sum('cantidad'))

#3)