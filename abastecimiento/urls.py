from abastecimiento import views

from django.urls import path, include, reverse, reverse_lazy
from django.views.generic.list import ListView

app_name = 'abastecimiento'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'productos/', views.ProductoList.as_view(), name='productos'),
    path(r'compra/', views.compra, name='compra'),
    path(r'compra/nueva/nueva', views.nueva, name='nueva'),
    path(r'compra/nueva/nueva/add', views.agrega_detalle, name='agrega_detalle'),
    path(r'compra/nueva', views.verifica, name='verifica'),
    path(r'producto/menu_buscar', views.menu_buscar, name='menu_buscar'),
    path(r'producto/buscar', views.buscar, name='buscar'),

    path(r'test/', views.test, name='test'),




    # path(r'reporte/boletas/detalle/<int:id>', views.detalle_boleta, name='detalle_boleta'),
    ]