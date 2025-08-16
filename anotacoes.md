deposito
transferencia

tabelas 
usuario
    nome
    sobrenome
    cpf/cnpj
    email
    senha
Carteira
    tipo usuario
    usuario
    saldo
Transfer
    pagador
    recebedor
    valor
    data da transferencia
    identificador unico



regras
cliente -> envia e recebe
lojista -> apenas recebe 
validar operacoes antes da transferencia
antes de finalizar a transferencia deve colsultar um autorizador GET
em caso de insconsistencia a operacao deve ser revertida e o dinheiro voltara para o usuario que enviou

endpoint
/transfer
{
'value': 100.0,
'payer': 4,
'payee': 15
}
