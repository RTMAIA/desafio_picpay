from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractBaseUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    tipo = models.CharField(max_length=7, choices=[('cliente', 'Cliente'),
                                                   ('lojista', 'Lojista')])
    first_name = models.CharField(_("nome"), max_length=150)
    last_name = models.CharField(_("sobrenome"), max_length=150)
    email = models.EmailField(_("email"), unique=True)
    cpf = models.IntegerField(unique=True, null=True, default=None )
    cnpj = models.IntegerField(unique=True, null=True, default=None)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    
    def set_password(self, raw_password):
        return super().set_password(raw_password)
    
    def check_password(self, raw_password):
        return super().check_password(raw_password)

class Carteira(models.Model):
    tipo_usuario = models.CharField(max_length=7)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(decimal_places=2, max_digits=7)

class Transfer(models.Model):
    pagador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagador', null=False)
    recebedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recebedor', null=False)
    valor = models.DecimalField(max_digits=7, decimal_places=2)
    data_transferencia = models.DateTimeField(auto_now_add=True)
    identificador = models.CharField(max_length=128, unique=True)
