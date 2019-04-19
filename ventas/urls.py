from . import views
from django.urls import path, include

urlpatterns = [
    path(r'', views.index, name='index'),

]
