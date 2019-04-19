from . import views
#from ventas.views import nueva,index
from django.urls import path, include


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'nueva/', views.nueva, name='nueva'),
    path(r'nueva/boleta/', views.boleta, name='boleta'),
    path(r'nueva/boleta/add', views.detalleadd, name='add'),
    path(r'nueva/factura/', views.factura, name='factura'),
    path(r'nueva/factura/add', views.detalleadd, name='add'),
    path(r'nueva/boleta/boletalista/',views.VentaList.as_view()),

]
