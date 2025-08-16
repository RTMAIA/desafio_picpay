from rest_framework import serializers
from .models import User, Transfer, Carteira
import requests

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['tipo', 'first_name', 'last_name', 'email', 'cpf', 'cnpj', 'password']

    def validate(self, attrs):
        if not attrs['cpf'] == None:
            if len(str(attrs['cpf'])) != 11:
                raise serializers.ValidationError('O cpf deve conter 11 digitos')
        if not attrs['cnpj'] == None:
            if len(str(attrs['cnpj'])) != 14:
                raise serializers.ValidationError('O cnpj deve conter 14 digitos')    
        return super().validate(attrs)


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['pagador', 'recebedor', 'valor']
    def validate(self, attrs):
        if attrs['pagador'].tipo != 'lojista':
            pagador = Carteira.objects.get(usuario_id=attrs['pagador'].id)
            recebedor = Carteira.objects.get(usuario_id=attrs['recebedor'].id)
            if pagador.saldo >= attrs['valor']:
                req = requests.get('https://util.devi.tools/api/v2/authorize')
                if not req.status_code == 200:
                    raise serializers.ValidationError('Algo inesperado aconteceu')
                pagador.saldo -= attrs['valor']
                recebedor.saldo += attrs['valor']
                pagador.save()
                recebedor.save()
                
                requisicao = requests.post('https://util.devi.tools/api/v1/notify')
                if not requisicao.status_code == 204:
                    raise serializers.ValidationError('Falha no envio da notificacao')
            else:
                raise serializers.ValidationError('Saldo insuficiente')
        else:
            raise serializers.ValidationError('Lojistas nao podem fazer transferencia')
        return super().validate(attrs)