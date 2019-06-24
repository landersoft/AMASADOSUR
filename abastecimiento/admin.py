from django.contrib import admin
from abastecimiento.models import Producto, Proveedor, Compra, DetalleCompra


###########################################################################
class AdminProveedor(admin.ModelAdmin):
    list_display = ["rut", "nombre", "direccion", "telefono", "email"]
    list_filter = ["rut"]
    #search_fields = ["rut", "nombre"]

    class Meta:
        model = Proveedor
        
#############################################################################
class AdminProducto(admin.ModelAdmin):
    list_display = ["id", "nombre", "descripcion", "precio_venta_unitario"]
    list_filter = ["id","nombre"]
    search_fields = ["id", "nombre"]

    class Meta:
        model = Producto

##############################################################################
class AdminCompra(admin.ModelAdmin):
    list_display = ["id", "fecha", "get_proveedor", "total"]
    list_filter = ["id","fecha"]
    search_fields = ["id"]
#################MUY IMPORTANTE FOREIGN KEY###########################
    def get_proveedor(self, obj):
        return obj.proveedor.nombre
        get_proveedor.short_description = 'Proveedor'
        get_proveedor.admin_order_field = 'proveedor_nombre'



    class Meta:
        model = Compra
###############################################################################
class AdminDetalleCompra(admin.ModelAdmin):
    list_display = ["id_compra", "id_producto", "cantidad", "precio_compra_unitario"]
    list_filter = ["id_compra","id_producto"]
    search_fields = ["id_compra"]

    class Meta:
        model = DetalleCompra


admin.site.register(Proveedor, AdminProveedor)
admin.site.register(Producto, AdminProducto)
admin.site.register(Compra, AdminCompra)
admin.site.register(DetalleCompra, AdminDetalleCompra)

