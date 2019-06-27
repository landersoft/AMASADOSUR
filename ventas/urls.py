from . import views
from ventas import views
from django.urls import path, include

app_name='ventas'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'nueva/', views.nueva, name='nueva'),
    #path(r'nueva/boleta/', views.boleta, name='boleta'),
    path(r'nueva/add', views.detalleadd, name='add'),
    path(r'nueva/menu2/', views.menu2, name='menu2'),    
    path(r'abrircaja/', views.abrircaja, name='abrircaja'),
    path(r'nueva/lista/', views.VentaList.as_view(), name='ventalist'),

    path(r'nueva/lista/pagar', views.pagar, name='pagar'),
    path(r'nueva/lista/formapago', views.formapago, name='formapago'),
    #path(r'abrircaja/formapago', views.formapago, name='formapago'),
    #path(r'nueva/formapago', views.formapago, name='formapago'),
    path(r'nueva/lista/documento', views.tipodocumento, name='tipodocumento'),
    path(r'nueva/lista/verifica', views.verifica, name='verifica'),
    path(r'nueva/lista/registrocliente', views.registracliente, name='registracliente'),
    path(r'cerrarcaja/', views.cerrarcaja, name='cerrarcaja'),
    path(r'cerrarcaja/arqueo', views.arqueo, name='arqueo'),
    path(r'cierracaja/', views.cierracaja, name='cierracaja'),

    path(r'estadisticas/', views.estadisticas, name='estadisticas'),
    path(r'reporte/boletas/', views.vista_boleta, name='vista_boleta'),
    path(r'reporte/boletas/cierre', views.vista_boleta_vivo, name='vista_boleta_vivo'),
    path(r'reporte/facturas/', views.vista_factura, name='vista_factura'),
    path(r'reporte/boletas/detalle/<int:id>', views.detalle_boleta, name='detalle_boleta'),
    path(r'reporte/facturas/detalle/<int:id>', views.detalle_factura, name='detalle_factura'),
    path(r'exito/', views.exito, name='exito'),
    path(r'test/', views.test, name='test'),
    
]

    # path(r'reporte/boletas/lista', views.detalle_boleta, name='detalle_boleta'),

    # https://stackoverflow.com/questions/7217811/query-datetime-by-todays-date-in-django

