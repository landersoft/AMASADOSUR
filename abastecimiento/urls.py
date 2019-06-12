from abastecimiento import views
from django.urls import path, include

app_name = 'abastecimiento'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'productos/', views.ProductoList.as_view(), name='productos'),
    ]