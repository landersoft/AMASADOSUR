from abastecimiento import views

from django.urls import path, include

app_name = 'abastecimiento'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'productos/', views.ProductoList.as_view(), name='productos'),
    path(r'compra/', views.compra, name='compra'),
    path(r'compra/nueva', views.nueva_compra, name='nueva_compra'),




    # path(r'reporte/boletas/detalle/<int:id>', views.detalle_boleta, name='detalle_boleta'),
    ]