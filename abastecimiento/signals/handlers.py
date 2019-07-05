from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import DetalleCompra

""" @receiver(post_save,sender=DetalleCompra)
def agrega_compra(instance, created, **kwargs):
    if created:
        
        #instance.id_producto.pmp = ((instance.id_producto.pmp*instance.id_producto.stock)+(instance.cantidad*instance.precio_unitario))/(instance.id_producto.stock+instance.cantidad)
        #instance.id_producto.save()
        instance.id_producto.stock += instance.cantidad
        instance.id_producto.save()
        #instance.id_producto.precio_actual=instance.id_producto.pmp+(instance.id_producto.pmp*0.5)
 """        #instance.id_producto.save()