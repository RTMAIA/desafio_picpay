from django.shortcuts import render
from .models import User, Carteira, Transfer
from rest_framework import generics
from .serializer import UserSerializer, TransferSerializer
from django.shortcuts import redirect
from django.db import transaction
import string
import random
# Create your views here.

def pagina_inicial(request):
    return redirect('api/users')

class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        usuario = User.objects.get(email=self.request.data['email'])
        carteira = Carteira(tipo_usuario=usuario.tipo, usuario=usuario, saldo=200)
        carteira.save()
        return super().perform_create(serializer)
    
class CreateTransfer(generics.CreateAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
        
    @transaction.atomic
    def perform_create(self, serializer):
        pagador = User.objects.get(id=self.request.data['pagador'])
        caracteres = string.ascii_letters + string.digits
        identificador = ''.join(random.choice(caracteres) for _ in range(128))
        
        serializer.save(pagador=pagador, identificador=identificador)