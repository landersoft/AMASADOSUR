
from django.contrib import admin
from ventas.models import Venta, Boleta, DetalleVenta, Factura, Cliente


# Register your models here.

class AdminCliente(admin.ModelAdmin):
    list_display = ["rut", "nombre", "direccion"]
    list_filter = ["rut"]
    search_fields = ["rut"]

    class Meta:
        model = Cliente


class AdminVenta(admin.ModelAdmin):
    list_display = ["id", "fecha", "total", "usuario"]
    list_filter = ["fecha", "usuario"]
    search_fields = ["usuario"]

    class Meta:
        model = Venta


class AdminBoleta(admin.ModelAdmin):
    list_display = ["id"]
    list_filter = ["id"]

    class Meta:
        model = Boleta


class AdminDetalleVenta(admin.ModelAdmin):
    list_display = ["id_detalleventa", "id_venta", "id_producto", "cantidad", "precio_venta_unitario"]
    list_filter = ["id_venta", "id_producto"]
    search_fields = ["id_venta"]

    class Meta:
        model = DetalleVenta


class AdminFactura(admin.ModelAdmin):
    list_display = ["id_venta", "id_cliente"]
    list_filter = ["id_venta", "id_cliente"]
    search_fields = ["id_venta", "id_cliente"]

    class Meta:
        model = Factura


admin.site.register(Venta, AdminVenta)
admin.site.register(Boleta, AdminBoleta)
admin.site.register(DetalleVenta, AdminDetalleVenta)
admin.site.register(Factura)
admin.site.register(Cliente, AdminCliente)
