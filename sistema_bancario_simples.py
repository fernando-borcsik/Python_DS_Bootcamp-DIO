import json
from datetime import date, datetime
import os

# Capturando o dia de hoje
HOJE = date.today().strftime('%Y-%m-%d')

# Texto de primeiro acesso
PRIMEIRO_ACESSO = """
Olá! Parece que você está acessando pela primeira vez, e ainda não possui uma conta. Para criá-la, basta escrever o seu nome:

=> """

# Constantes
LIMITE_POR_SAQUE = 500
LIMITE_DIARIO_SAQUES = 3

# Abertura ou criação do histórico da conta
try:
    with open('sistema_bancario_simples_historico.json', 'r') as fp:
        historico = json.load(fp)
    nome = historico['nome']
    saldo = historico['saldo']
    extrato = historico['extrato']
    saques = historico['saques']
    n_saques = saques.count(HOJE)
except:
    historico = {}
    nome = input(PRIMEIRO_ACESSO)
    historico['nome'] = nome
    saldo = 0
    historico['saldo'] = saldo
    n_saques = 0
    saques = []
    historico['saques'] = saques
    extrato = {'data': [], 'texto': []}
    historico['extrato'] = extrato

# Texto do menu
INICIO = f"""
Bem vindo, {nome}! Escolha a opção desejada no menu abaixo:
"""

MENU = """
Digite [d] para depositar;
Digite [s] para sacar;
Digite [e] para conferir o extrato e o saldo de sua conta;
Digite [nome] para alterar o nome da conta;
Digite [deletar] para deletar a conta; 
Digite [q] caso deseje encerrar.

=> """

print(INICIO)

zerar_conta = ''

# Programa com as operações disponíveis
while True:

    opcao = input(MENU)

    if opcao == 'd':
        
        valor = input('\nDigite o valor que deseja depositar, ou [c] para cancelar a operação: ')

        while True:
            if valor == 'c':
                print('\nOperação cancelada.')
                break
            else:
                try:
                    valor = float(valor)
                    if valor <= 0:
                        valor = input('\nPor favor, digite um valor maior do que zero, ou [c] para cancelar a operação: ')
                    else:
                        confirmar = input(f'\nConfirma depósito no valor de R$ {valor:.2f}? [s/n]: ')

                        while confirmar not in ['s', 'n']:
                            confirmar = input('\nOpção inválida. Digite [s] para confirmar o depósito ou [n] para cancelar: ')

                        if confirmar == 's':
                            saldo += valor
                            data_deposito = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            extrato['data'].append(data_deposito)
                            extrato['texto'].append(f'Depósito realizado no valor de R$ {valor:.2f}')
                            print(f'\nDepósito de R$ {valor:.2f} realizado com sucesso!')
                            break
                        else:
                            print('\nDepósito cancelado.')
                            break
                except:
                    valor = input('\nPor favor, digite um valor numérico para seu depósito, ou [c] para cancelar a operação: ')

    elif opcao == 's':

        if n_saques >= LIMITE_DIARIO_SAQUES:
            print(f'\nA quantidade limite de {LIMITE_DIARIO_SAQUES} saques por dia já foi atingida hoje!')
        else:
            valor = input(f'\nNúmero de saques disponíveis hoje: {LIMITE_DIARIO_SAQUES - n_saques}.\nDigite o valor que deseja sacar, ou [c] para cancelar a operação: ')

            while True:
                if valor == 'c':
                    print('\nOperação cancelada.')
                    break
                else:
                    try:
                        valor = float(valor)
                        if valor <= 0:
                            valor = input('\nPor favor, digite um valor maior do que zero, ou [c] para cancelar a operação: ')
                        elif valor > LIMITE_POR_SAQUE:
                            valor = input(f'\nO valor digitado de R$ {valor:.2f} excede o limite por saque de R$ {LIMITE_POR_SAQUE:.2f}.\nPor favor, digite um valor válido, ou [c] para cancelar a operação: ')
                        elif valor > saldo:
                            valor = input(f'\nO valor digitado de R$ {valor:.2f} excede o saldo atual de R$ {saldo:.2f}.\nPor favor, digite um valor válido, ou [c] para cancelar a operação: ')
                        else:
                            confirmar = input(f'\nConfirma saque no valor de R$ {valor:.2f}? [s/n]: ')

                            while confirmar not in ['s', 'n']:
                                confirmar = input('\nOpção inválida. Digite [s] para confirmar o saque ou [n] para cancelar: ')

                            if confirmar == 's':
                                saldo -= valor
                                n_saques += 1
                                data_saque = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                historico['saques'].append(HOJE)
                                extrato['data'].append(data_saque)
                                extrato['texto'].append(f'Saque realizado no valor de R$ {valor:.2f}')
                                print(f'\nSaque de R$ {valor:.2f} realizado com sucesso!')
                                break
                            else:
                                print('\nSaque cancelado.')
                                break
                    except:
                        valor = input('\nPor favor, digite um valor numérico para seu depósito, ou [c] para cancelar a operação: ')

    elif opcao == 'e':
        print('\n############################## EXTRATO ##############################')
        if len(extrato['data']) == 0:
            print('Ainda não há movimentações nessa conta.')
        else:
            for data, texto in zip(extrato['data'], extrato['texto']):
                print(data, texto, sep='\t')
        print(f'\nSaldo total: {saldo:.2f}')
        print('#####################################################################\n')

    elif opcao == 'q':
        sair = input('\nTem certeza que deseja sair? [s/n]: ')
        
        while sair not in ['s', 'n']:
            sair = input('\nOpção inválida. Digite [s] caso deseje sair ou [n] para voltar ao menu de opções: ')
            
        if sair == 's':
            break

    elif opcao == 'nome':
        nome = input(f'\nSeu nome atual está registrado como {nome}. Digite o novo nome que deseja para sua conta: ')
        print(f'\nNome alterado para {nome}.')
        historico['nome'] = nome

    elif opcao == 'deletar':
        zerar_conta = input(f'\nPara deletar sua conta, você deve zerar antes o seu saldo. Deseja realizar a retirada de seu saldo total de R$ {saldo:.2f}? [s/n]: ')

        while zerar_conta not in ['s', 'n']:
            zerar_conta = input('\nOpção inválida. Digite [s] caso deseje retirar todo o seu saldo e deletar sua conta ou [n] para cancelar: ')

        if zerar_conta == 's':
            print(f'\nSaldo total retirado. Sua conta foi excluída. Adeus, {nome}!')
            break
        else:
            print('\nRetirada do saldo total e exclusão da conta cancelados!')

    else:
        print('\nEntrada inválida. Confira as opções no menu:')


if zerar_conta != 's':
    # Salvando histórico de operações:
    historico['saldo'] = saldo

    with open('sistema_bancario_simples_historico.json', 'w') as fp:
        json.dump(historico, fp, indent=4)

    print(f'\nAté logo, {nome}!')
else:
    os.remove('sistema_bancario_simples_historico.json')