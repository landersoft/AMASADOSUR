from abastecimiento import views
from django.urls import path, include

app_name = 'abastecimiento'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'productos/', views.ProductoList.as_view(), name='productos'),
    path(r'productos/crear', views.ProductoCreate.as_view(), name='crear_producto'),
    # path(r'reporte/boletas/detalle/<int:id>', views.detalle_boleta, name='detalle_boleta'),
    ]