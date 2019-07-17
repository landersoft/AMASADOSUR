from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from .models import Producto, Proveedor, Compra, DetalleCompra


@login_required
def index(request):
    return render(request, 'ventas/menu2.html')




@method_decorator(login_required, name='dispatch')
class ProductoList(ListView):
    model = Producto
    paginate_by = 20
    template_name = 'abastecimiento/productos.html'
    context_object_name = 'productos'





class CrearCompra(CreateView):
    pass


    

@login_required
class ListadoCompras(ListView):
    model = Compra
    template_name = 'abastecimiento/compras.html'
    context_object_name = 'compras'


@login_required
def compra(request):
    return render(request, "abastecimiento/compra.html")

@login_required
def nueva(request):
    if request.method == "POST":
        documento=request.POST.get('dcto')
        proveedor = Proveedor.objects.get(rut=request.POST.get('rut'))

        try:
            Compra.objects.get(documento=documento,proveedor=proveedor)
            mesj="Documento ya ingresado"
            return render(request,'ventas/info.html',{'mesj': mesj})
        except Compra.DoesNotExist:
            documento = request.POST.get('dcto')
            fecha=request.POST.get('fecha')
            proveedor=Proveedor.objects.get(rut=request.POST.get('rut'))
            usuario=request.user
            nueva_compra=Compra(documento=documento,fecha=fecha,proveedor=proveedor,usuario=usuario)
            nueva_compra.save()
            print(Compra.objects.latest('id'))


            context={
                'documento': documento,
                'fecha': fecha,
                'dcto': documento,
                'rut': proveedor.rut,
                'nombre': proveedor.nombre,
                'id': Compra.objects.latest('id'),
                'usuario': usuario,
            }
        return render(request,'abastecimiento/compra.html',context)

@login_required
def agrega_detalle(request):
    if request.method == 'POST':
        
        id_compra2 = request.POST.get('id_compra')
        id_2 = Compra.objects.get(id=id_compra2)
        codigo=request.POST.get('codigo')
        try:
            producto = Producto.objects.get(codigo_barras=codigo)
        except Producto.DoesNotExist:
            msj2="Producto No existe"
            return render(request,'ventas/venta.error.html', {'msj2': msj2})
            
        #consulta si ya se ingresó el producto
        try:
            consulta = DetalleCompra.objects.get(id_producto=producto,id_compra=id_2)
            mesj2 = "Producto ya ingresado"
            context ={
                'msj2': msj2,
            }
            return render(request, 'abastecimiento/venta.error.html', context)
        
        except DetalleCompra.DoesNotExist:
            print(producto.id)
            lote = request.POST.get('lote')
            fecha_vencimiento = request.POST.get('fecha_vencimiento')
            cantidad = request.POST.get('cantidad')
            precio_compra_unitario = request.POST.get('precio')
            nuevo_detalle = DetalleCompra.objects.create(id_compra=id_2, id_producto=producto, lote=lote,fecha_vencimiento = fecha_vencimiento, cantidad= cantidad,precio_compra_unitario = precio_compra_unitario)
            productos = DetalleCompra.object.filter()

            detalles = DetalleCompra.objects.filter(id_compra=id_2.id)
            documento = request.POST.get('dcto')
            proveedor = Proveedor.objects.get(rut=request.POST.get('rut'))
            fecha=request.POST.get('fecha')
            print(fecha)
            usuario=request.user

            

            context={
                    
                    'detalles': detalles,
                    'fecha': fecha,
                    'dcto': documento,
                    'rut': proveedor.rut,
                    'nombre': proveedor.nombre,
                    'id': id_2.id,
                    'usuario': usuario,
                }
            return render(request, 'abastecimiento/compra.html', context)

@login_required
def verifica(request):
    if request.method=="POST":
        rut_proveedor = request.POST['rut']
        print(rut_proveedor)
        try:
            proveedor = Proveedor.objects.get(rut=rut_proveedor)
            print(proveedor.nombre)
            
            context={
                'nombre': proveedor.nombre,
                'rut': proveedor.rut,
                'usuario': request.user
            }
            return render(request, 'abastecimiento/compra.html', context)
        except Proveedor.DoesNotExist:
            proveedor=None
            mesj = "Proveedor no existe,redirigiendo"
            context={
                'mesj2': mesj
            }
            return render(request,'ventas/info.html',context)

@login_required
def test(request):
    return render(request, 'abastecimiento/test.html')