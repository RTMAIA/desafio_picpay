from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('api/users', views.CreateUser.as_view(), name='createuser'),
    path('', views.pagina_inicial, name='redirect'),
    path('api/transfer', views.CreateTransfer.as_view(), name='createtransfer')


]
