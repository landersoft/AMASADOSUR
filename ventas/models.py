from django.db import models
from datetime import date
from django.conf import settings
from django.db import models
from abastecimiento.models import Producto


class Cliente(models.Model):
    rut = models.IntegerField(null=False, blank=False)
    nombre = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=100, null=False, blank=False)
    def __str__(self):
        return str(self.nombre)

class Caja(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null=True)
    hora_a = models.DateTimeField(blank=True)
    hora_c = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=10)
    monto_inicial = models.IntegerField()
    monto_final = models.IntegerField(blank=True, null=True)
    caja_modulo = models.CharField(max_length=20, null=False, blank=False)
    def __str__(self):
        return (self.estado)

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now=False, auto_now_add=True)
    total = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null=True)
    producto = models.ManyToManyField("abastecimiento.Producto", through='DetalleVenta')
    forma_pago = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return str(self.id)
   
class DetalleVenta(models.Model):
    id_detalleventa = models.AutoField(primary_key=True)
    id_venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    id_producto = models.ForeignKey('abastecimiento.Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_venta_unitario = models.IntegerField()

    class Meta:
        ordering = ["id_venta"]
        verbose_name = 'Detalle de Ventas'
        verbose_name_plural = 'Detalle de Ventas'

        def __str__(self):
            return str(self.id_detalleventa)
            

class Factura(models.Model):
    id_venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    id_cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)


class Boleta(models.Model):
    id_venta = models.ForeignKey('Venta', on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id)
