from . import views
#from ventas.views import nueva,index
from django.urls import path, include


urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'nueva/', views.nueva, name='nueva'),
    path(r'nueva/boleta/', views.boleta, name='boleta'),
    path(r'nueva/add', views.detalleadd, name='add'),
    #path(r'nueva/factura/', views.factura, name='factura'),
    #path(r'nueva/factura/add', views.detalleadd, name='add'),
    path(r'nueva/lista/',views.VentaList.as_view()),
    path(r'nueva/lista/pagar', views.pagar, name='pagar'),
    path(r'nueva/lista/formapago', views.formapago, name='formapago'),
    path(r'nueva/lista/documento', views.tipodocumento, name='tipodocumento'),
    path(r'nueva/lista/verifica', views.verifica, name='verifica'),

]
