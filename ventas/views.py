from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from abastecimiento.models import DetalleCompra
from .models import Venta, Producto, DetalleVenta, Boleta, Factura, Cliente, Caja
from django.views.generic import ListView
from django.db.models import Q,F
from django.db.models import Sum, IntegerField
from django.shortcuts import render_to_response
from django.template import RequestContext
from .forms import RegCliente
from django.contrib.auth import get_user
from datetime import date, datetime





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
        try:
                usuario=get_user(request)
                caja = Caja.objects.get(usuario=usuario,estado="abierta")
                print(caja)
                hoy=datetime
                if caja.hora_a.date()<datetime.now().date():
                    mesj="Caja no cerrada la ultima jornada. Por favor cerrar"
                    return render(request,'ventas/cerrarcaja.html', {'mesj': mesj})

                nueva_venta = Venta(usuario=request.user)
                nueva_venta.save()
                codigo_venta = Venta.objects.latest('id')
                print(codigo_venta)
                return render(request, 'ventas/detalleventa_list.html')

        except Caja.DoesNotExist:
                caja = None
                mesj = "¡Por favor abrir caja!222"
                return render(request,'ventas/nocaja.html',{'mesj':mesj})


#3 eligió boleta 
@login_required
def boleta(request):

    if request.method == 'POST':
        nueva_venta = Venta(usuario=request.user)
        nueva_venta.save()
        codigo_venta = Venta.objects.latest('id')
        print(codigo_venta)
    return render(request, 'ventas/venta.html')

@login_required
def detalleadd(request):

    if request.method == 'POST':  
        
        try:
                de_producto = Producto.objects.get(pk=request.POST.get('textinput'))
        except Producto.DoesNotExist:
                de_producto = None
                msj="Producto No existe"
                return render(request,'ventas/venta.error.html', {'msj': msj})

        flotante = (request.POST['textinput'])
        de_venta = Venta.objects.last()
        print(de_venta.id)
        print(de_producto.id)      
        # consulta para saber si hay mas de este mismo producto
        obj = DetalleVenta.objects.filter(id_producto=de_producto.id, id_venta=de_venta.id).first()
        
        # query = DetalleVenta.objects.filter(id_producto = flotante, id_venta = de_venta).count()
        precio = Producto.objects.get(id=flotante).precio_venta_unitario
        
        if obj is None:
            det_venta = DetalleVenta()
            det_venta.id_producto=de_producto
            det_venta.id_venta=de_venta
            cero = request.POST.get('cantidad')
            if cero=='':
                det_venta.cantidad = 1
            else:
                det_venta.cantidad = request.POST.get('cantidad')
                det_venta.precio_venta = precio
                det_venta.save()
        else:
            det_venta = DetalleVenta.objects.get(id_producto=de_producto, id_venta=de_venta)
            cero = request.POST.get('cantidad')
            if cero=='':
                det_venta.cantidad += 1
            else:
                det_venta.cantidad += int(request.POST.get('cantidad'))
            det_venta.save()

        print(de_producto.nombre)
        print(precio)
        print(det_venta.cantidad)
        # print((det_venta.cantidad * det_venta.precio_venta))
        total2 = DetalleVenta.objects.filter(id_venta=Venta.objects.latest('id')).aggregate(suma=Sum(F('precio_venta')*F('cantidad')))
        print("total consulta")
        de_venta.total = total2["suma"]
        print(total2["suma"])
        contador = len(total2)
        de_venta.save()

        subtotal = Venta.objects.last()
        return HttpResponseRedirect('lista/')


""" def boletaofactura(request):
        if request.method == 'POST':
                tipodocumento = request.POST['documento']
                if tipodocumento == 'boleta':
                        nueva_boleta = Boleta(id_venta=Venta.objects.latest('id')) """

@login_required
def formapago(request):
    if request.method == 'POST':
        forma = request.POST.get('exampleRadios')
        print("esta el la forma")
        print(forma)
        de_venta = Venta.objects.last()
        if forma =='option1':               
                de_venta.forma_pago = 'Efectivo'
                #nueva_boleta = Boleta(id_venta=Venta.objects.latest('id'))
        else:
                de_venta.forma_pago = 'Tarjeta'

        de_venta.save()
        
        tipo = request.POST.get('fp')
        print("esta es el tipo")
        print(tipo)
        if tipo == "boleta":
            nueva_boleta = Boleta(id_venta=Venta.objects.latest('id'))
            nueva_boleta.save()
            boleta2 = Boleta.objects.all().last()
            print("esta es la boleta")
            print(boleta2.id)
            venta = Boleta.objects.latest('id').id_venta
            print("esta es la venta")
            print(venta)
            detalles = DetalleVenta.objects.filter(id_venta=venta).values('id_producto','cantidad')
            print(detalles)
            for detalle in detalles:
                #instance.id_producto.stock += instance.cantidad
                stock_actual=Producto.objects.get(id=detalle['id_producto']).stock
                print(stock_actual)
                #producto = Producto.objects.get(id=detalle['id_producto']).stock-=detalle['cantidad']
                producto = Producto.objects.get(id=detalle['id_producto'])
                producto.stock -= detalle['cantidad']
                producto.save()

            # return render(request, 'ventas/exito.html', {'boleta2': boleta2})
            url = reverse('ventas:exito')
            return HttpResponseRedirect(url)

            #url = reverse('ventas:detalle_boleta', kwargs={'id': boleta2.id})
            #return HttpResponseRedirect(url)
        else:
                return render(request, 'ventas/verifica.html')
        





        
@login_required
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
@login_required
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

@login_required
def verifica(request):
        if request.method == 'POST':
                rut = request.POST['rut']
                try:
                        cliente = Cliente.objects.get(rut=request.POST['rut'])
                except Cliente.DoesNotExist:
                        cliente = None
                        return HttpResponseRedirect('registrocliente')


                print("este es el id del cliente " +str(cliente))
                                
                if cliente!=(None):
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


                        return render(request, 'ventas/exito.html')
                else:
                        return HttpResponseRedirect('registrocliente')
                
#https://es.stackoverflow.com/questions/95569/recuperar-objectos-de-un-modelo-en-django

@login_required
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

                return render(request, 'ventas/exito.html')
                #este te entrega el id de venta
                
                

        return render(request, "ventas/registrocliente.html", context)

@login_required
def estadisticas(request):
            ############################TOTAL VENTAS OK#########################################
        ventas=Venta.objects.filter(id__in=Boleta.objects.values('id_venta'))|Venta.objects.filter(id__in=Factura.objects.values('id_venta'))
        #ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id_venta_id')))
        ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id')))
        totalventas = ven.aggregate(totalventas=Sum(F('precio_venta')*F('cantidad')))['totalventas']
        print(totalventas)

            ############################Cantidad de productos vendidos x id############################
        ventas= Venta.objects.filter(id__in=Boleta.objects.values('id_venta'))| Venta.objects.filter(id__in=Factura.objects.values('id_venta'))
        ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id')))
        #ven2 = Producto.objects.filter(id__in=DetalleVenta.objects.values('id_producto')).values('nombre','detalleventa__cantidad')
        ven2 = ven.values('id_producto_id').order_by('id_producto_id').annotate(total=Sum('cantidad'))
        #cantidad_id = ven.values().order_by('detalleventa__id_producto').annotate(total=Sum('detalleventa__cantidad'))
        print('esta es la cantidad_id')
        #print(cantidad_id)
        nombre = Producto.objects.filter(id__in=ven2.values('id_producto_id'))
            ###########################Utilidad Neta###############################################
        
        ventas=Venta.objects.filter(id__in=Boleta.objects.values('id_venta'))| Venta.objects.filter(id__in=Factura.objects.values('id_venta'))
        #ventas = Boleta.objects.all()
        ven = DetalleVenta.objects.filter(id_venta__in=(ventas.values('id')))
        cantidades = ven.values('id_producto_id').order_by('id_producto_id').annotate(total=Sum('cantidad'))
        precio=DetalleCompra.objects.filter(id_producto_id__in=ven2.values('id_producto_id')).values('id_producto_id','precio_unitario_compra')

        pre=list(precio)
        can=list(cantidades)
        costo=0

        print('este es el pre')
        print(pre)

        indice=0
        suma=0
        print (str(len(cantidades)))

        for i in range(len(can)):
            if can[i]['id_producto_id']==pre[i]['id_producto_id']:
                suma=suma+(can[i]['total']*pre[i]['precio_unitario_compra'])

        print(suma)
        print('este es el costo')


        utilidad=totalventas-suma


        #utilidad=tv[indice]['totalventas']-suma
        print(utilidad)
        #for indice in cantidades.__len__():
        #    indice+=indice
        #    if cantidades.values('id_producto_id')[indice]==pre[indice]['id_producto_id']:
        #            costo=costo+(cantidades.values('cantidad'))* pre[indice]['precio_unitario_compra']
        #print(costo)
            #utilidad_neta=totalventas-costo
            #,{'cantidad_id': cantidad_id}




            
        return render(request,'ventas/estadisticas.html',{'totalventas': totalventas ,'ven2': ven2,'utilidad': utilidad , nombre:'nombre'})


@login_required
def vista_boleta(request):
    boletas=Venta.objects.filter(id__in=Boleta.objects.values('id_venta')).values('boleta__id','boleta__id_venta','forma_pago','total')
    boletas=boletas.order_by('boleta')
    return render(request,'ventas/vista_boleta.html',{'boletas': boletas})

@login_required
def vista_factura(request):
    facturas=Venta.objects.filter(id__in=Factura.objects.values('id_venta')).values('factura__id','factura__id_venta','forma_pago','total')
    facturas=facturas.order_by('factura')
    return render(request, 'ventas/vista_factura.html', {'facturas': facturas})

@login_required
def detalle_factura(request,id):
    factura= Factura.objects.filter(id=id)
    cliente= Cliente.objects.filter(id__in=Factura.objects.values('id_cliente')).values('id','nombre','rut','direccion').filter(factura__id=id)
    venta3 = Venta.objects.filter(id__in=factura.values('id_venta_id'))
    detalle = Venta.objects.filter(id__in=Factura.objects.values('id_venta_id')).values('factura__id','id','detalleventa__id_detalleventa','detalleventa__cantidad', 'producto__nombre', 'producto__id','total','detalleventa__precio_venta').annotate(subto=F('detalleventa__cantidad')*F('detalleventa__precio_venta')).filter(factura__id=id)
    iva = venta3.values('total').annotate(iva=F('total')*0.19)
    supertotal=venta3.values('total').annotate(iva=F('total')*0.19).annotate(supertotal=Sum(F('total')+F('iva')))

    return render(request, 'ventas/detalle_factura.html',{'factura':factura, 'cliente': cliente, 'venta3': venta3, 'detalle': detalle, 'iva':iva, 'supertotal':supertotal})

@login_required
def detalle_boleta(request, id):
    boleta= Boleta.objects.filter(id=id)
    #print(boleta)
    venta2 = Venta.objects.filter(id__in=boleta.values('id_venta_id'))
    #print(venta2)
    detalle=Venta.objects.filter(id__in=Boleta.objects.values('id_venta')).values('boleta__id','id','detalleventa__id_detalleventa','detalleventa__cantidad','producto__nombre','producto__id','total','detalleventa__precio_venta').annotate(suto=F('detalleventa__cantidad')*F('detalleventa__precio_venta')).filter(boleta__id=id)
    #detalle=(Producto.objects.filter(id__in=DetalleVenta.objects.values('id_producto_id')).values('id','nombre','detalleventa__cantidad','detalleventa__precio_venta')).filter(detalleventa__id_venta__in=venta2.values('id'))
    #detalle = DetalleVenta.objects.filter(id_venta__in=venta2.values('id'))
    #a=Venta.objects.filter(id__in=Boleta.objects.values('id_venta')).values('boleta__id','id','detalleventa__id_detalleventa','detalleventa__cantidad','producto__nombre','producto__id','total').filter(boleta__id=1)
    
    print(detalle)
    #(Producto.objects.filter(id__in=DetalleVenta.objects.values('id_producto_id')).values('id','nombre','detalleventa__cantidad','detalleventa__precio_venta')).filter(detalleventa__id_venta=1)
    return render(request,'ventas/detalle_boleta.html', {'venta2':venta2 ,'detalle':detalle, 'boleta':boleta })
    
@login_required
def exito(request):
    boleta2 = Boleta.objects.all().last()
    # url = reverse('ventas:detalle_boleta', kwargs={'id': boleta2.id})
    # return HttpResponseRedirect(url)
    boleta_dict = {
        'boleta2': boleta2
    }
    return render(request, 'ventas/exito.html', boleta_dict)

@login_required
def menu2(request):
        return render(request,'ventas/menu2.html')

@login_required
def abrircaja(request):
        if request.method == 'POST':
                try:
                        usuario=get_user(request)
                        caja = Caja.objects.get(usuario=usuario,estado="abierta")
                        print(caja)
                        hoy=datetime
                        if caja.hora_a.date()<datetime.now().date():
                                mesj="Caja no cerrada la ultima jornada. Por favor cerrar"
                                return render(request,'ventas/cerrarcaja.html', {'mesj': mesj})
                        elif caja.hora_a.date()==datetime.now().date() and caja.hora_c.date()==datetime.now().date():
                                mesj="Caja cerrada por hoy"
                                return render(request,'ventas/info.html',{'mesj': mesj})

                except Caja.DoesNotExist:        
                        newcaja = Caja()
                        #newcaja.caja_modulo = request.META['HTTP_X_FORWARDED_FOR']
                        newcaja.caja_modulo = request.META.get('REMOTE_ADDR')
                        #request.META.get(‘REMOTE_ADDR’)
                        #newcaja.caja_modulo = request.get_host()
                        usuario = get_user(request)
                        newcaja.usuario=usuario
                        newcaja.hora_a=datetime.now()
                        newcaja.estado="abierta"
                        newcaja.monto_inicial=request.POST.get('monto')
                        newcaja.save()
                        nueva_venta = Venta(usuario=request.user)
                        nueva_venta.save()
                        codigo_venta = Venta.objects.latest('id')
                        return render(request, 'ventas/detalleventa_list.html')
        else:   
                try:
                        usuario=get_user(request)
                        caja = Caja.objects.get(usuario=usuario,estado="abierta")
                        print(caja)
                        hoy=datetime
                        if caja.hora_a.date()<datetime.now().date():
                                mesj="Caja no cerrada la ultima jornada. Por favor cerrar"
                                return render(request,'ventas/cerrarcaja.html', {'mesj': mesj})
                        elif caja.hora_a.date()==datetime.now().date() and caja.hora_c.date()==datetime.now().date():
                                mesj="Caja cerrada por hoy"
                                return render(request,'ventas/info.html',{'mesj': mesj})
                except:
                        return render(request, 'ventas/nocaja.html')


        


@login_required
def cerrarcaja(request):
        if request.method == 'POST':
            usuario = get_user(request)
            print(usuario)
            try:
                caja = Caja.objects.get(usuario=usuario, estado="abierta")
                print(caja.id)
                caja.hora_c = datetime.now()
                caja.estado = "cerrado"
                caja.save()
                apertura = Caja.objects.filter(id=caja.id)[0].hora_a
                cierre = Caja.objects.filter(id=caja.id)[0].hora_c
                #caja.monto_final = Venta.objects.values('total').annotate(total_venta=Sum('total'))
                total = Venta.objects.filter(fecha__range=(apertura, cierre)).exclude(total__isnull=True).aggregate(totality=Sum('total'))
                print("te extraño caja1")
                print(total)
                #print("este es el totality: " + caja2['totality'])
                caja.monto_final = total['totality']
                caja.save()
                # return render(request, 'ventas/arqueo.html')
                url = reverse('ventas:arqueo')
                print(url)
                return HttpResponseRedirect(url)
            except Caja.DoesNotExist:
                    caja = None
                    mesj = "Usuario no presenta cajas abiertas"
                    context = {
                        'mesj': mesj
                    }


                    return render(request, 'ventas/nocaja.html', context)

@login_required
def cierracaja(request):
    return render(request, 'ventas/cerrarcaja.html')


@login_required
def arqueo(request):
        usuario = get_user(request)
        print(usuario)

        #caja = Caja.objects.latest(usuario=usuario, estado="cerrada")
        caja = Caja.objects.filter(usuario=usuario, estado="cerrado").latest('id')
        caja = Caja.objects.get(id=caja.id)
        print(caja.id)
        print(caja.usuario)
        if caja.hora_a.date() == datetime.now().date() and caja.hora_c.date() == datetime.now().date():

            caja_id = caja.id
            fecha = caja.hora_a.date()
            usuario = caja.usuario
            print(usuario)
            hora = datetime.now()
            hora = hora.time()
            print(hora)
            hora_apertura = caja.hora_a.time()
            hora_cierre = caja.hora_c.time()
            total_efectivo = Venta.objects.filter(fecha__range=(caja.hora_a,caja.hora_c)).exclude(total__isnull=True,forma_pago='Tarjeta').aggregate(totality=Sum('total'))
            total_efectivo = total_efectivo
            total_tarjeta = Venta.objects.filter(fecha__range=(caja.hora_a,caja.hora_c)).exclude(total__isnull=True,forma_pago='Efectivo').aggregate(totality=Sum('total'))
            monto_inicial = caja.monto_inicial
            monto_final = caja.monto_final
            caja_modulo = caja.caja_modulo
            print(caja_modulo)

            caja_dict = {
                'caja_id': caja_id ,
                'fecha': fecha,
                'usuario': usuario,
                'hora': hora,
                'hora_apertura': hora_apertura,
                'hora_cierre': hora_cierre,
                'total_efectivo': total_efectivo,
                'total_tarjeta': total_tarjeta,
                #totality=Sum('total'))
                'monto_inicial': monto_inicial,
                'monto_final': monto_final,
                'caja_modulo': caja_modulo,
            }

            return render(request, 'ventas/arqueo.html', caja_dict)
        else:
            mesj = "Caja no cerrada el dia de hoy"
            return render(request, 'ventas/cerrarcaja.html', {'mesj': mesj})
                

@login_required
def test(request):
    return render(request, "abastecimiento/compras.html")