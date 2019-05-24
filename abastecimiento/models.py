from django.db import models
from django.conf import settings


class Proveedor(models.Model):
    rut = models.CharField(max_length=10, blank=False, null=False)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=False, null=False)
    telefono = models.IntegerField()
    email = models.EmailField(max_length=254)
    class Meta:
        verbose_name_plural = "Proveedores"

        def __str__(self):
            return str(self.rut)


class Producto(models.Model):
    nombre = models.CharField(max_length=10, blank=False, null=False)
    descripcion = models.CharField(max_length=30, blank=False, null=False)
    precio_actual = models.IntegerField()
    pmp = models.IntegerField()
    stock = models.IntegerField(default=0, editable=False)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    documento = models.CharField(max_length=20, blank=False, null=False)
    fecha = models.DateField(auto_now=True)
    proveedor = models.ForeignKey(
        'Proveedor', related_name='proveedores', on_delete=models.PROTECT)
    total = models.IntegerField()
    producto = models.ManyToManyField('Producto', through='DetalleCompra')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return str(self.id)


class DetalleCompra(models.Model):
    id_compra = models.ForeignKey('Compra', related_name='compra', on_delete=models.CASCADE)
    id_producto = models.ForeignKey(
        "Producto", related_name='producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.IntegerField()

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Detalle de Compras"
        verbose_name = "Detalle de Compra"

        def __str__(self):
            return self.id

