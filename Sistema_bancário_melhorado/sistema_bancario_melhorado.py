import json
from datetime import date, datetime
import getpass

# Constantes
LIMITE_POR_SAQUE = 500
LIMITE_DIARIO_SAQUES = 3
AGENCIA = '0001'
MAX_TENTATIVAS_LOGIN = 3

# Classe que define propriedades de um usuário do sistema bancário.
class Usuario:

    def __init__(self, nome, data_nascimento, cpf, endereco, senha):

        self.nome = nome
        self.data_nascimento = data_nascimento
        self.__cpf = cpf
        self.endereco = endereco
        self.senha = senha

    @property
    def cpf(self):
        return self.__cpf
    
    def to_dict(self):
        return {
            'nome': self.nome,
            'data_nascimento': self.data_nascimento,
            'cpf': self.cpf,
            'endereco': self.endereco,
            'senha': self.senha
        }
    
    @staticmethod
    def from_dict(dados):
        return Usuario(dados['nome'], dados['data_nascimento'], dados['cpf'], dados['endereco'], dados['senha'])
    
    def __eq__(self, other):
        return self.nome == other.nome and self.cpf == other.cpf
    
    def __repr__(self):
        return f'Usuário {self.nome}, CPF {self.cpf}'
    
    def __str__(self):
        return f'{self.nome}, {self.cpf}'
    

# Classe que define propriedades de uma conta bancária.
class Conta:

    def __init__(self, usuario, agencia, numero, apelido=None, historico={}, lim_por_saque=LIMITE_POR_SAQUE, lim_diario_saques=LIMITE_DIARIO_SAQUES):

        self.__usuario = usuario
        self.__agencia = agencia
        self.__numero = numero
        self.apelido = apelido
        self.historico = historico
        self.__lim_por_saque = lim_por_saque
        self.__lim_diario_saques = lim_diario_saques
        if not historico:
            self.historico['saldo'] = 0
            self.historico['saques'] = []
            self.historico['extrato'] = {'data': [], 'texto': []}
        
    @property
    def usuario(self):
        return self.__usuario
    
    @property
    def agencia(self):
        return self.__agencia
    
    @property
    def numero(self):
        return self.__numero
    
    @property
    def lim_por_saque(self):
        return self.__lim_por_saque
    
    @property
    def lim_diario_saques(self):
        return self.__lim_diario_saques
    
    def to_dict(self):
        return {
            'usuario': self.usuario.to_dict(),
            'agencia': self.agencia,
            'numero': self.numero,
            'apelido': self.apelido,
            'historico': self.historico,
            'lim_por_saque': self.lim_por_saque,
            'lim_diario_saques': self.lim_diario_saques
        }
    
    @staticmethod
    def from_dict(dados):
        usuario = Usuario.from_dict(dados['usuario'])
        return Conta(usuario, dados['agencia'], dados['numero'], dados['apelido'], dados['historico'])

    def __eq__(self, other):
        return self.agencia == other.agencia and self.numero == other.numero
    
    def __repr__(self):
        return f'Agência {self.agencia}, conta número {self.numero}'
    
    def __str__(self):
        return f'{self.agencia}, {self.numero}'


# Função para salvar os usuários e contas em um arquivo JSON.
def salvar_usuarios_contas(usuarios, contas):
    dados = {
        'usuarios': [usuario.to_dict() for usuario in usuarios],
        'contas': [conta.to_dict() for conta in contas]
    }
    with open('dados_usuarios_contas.json', 'w') as file:
        json.dump(dados, file)


# Função para carregar os usuários e contas do arquivo JSON.
def carregar_usuarios_contas():
    with open('dados_usuarios_contas.json', 'r') as file:
        dados = json.load(file)
        usuarios = [Usuario.from_dict(dados_usuario) for dados_usuario in dados['usuarios']]
        contas = [Conta.from_dict(dados_conta) for dados_conta in dados['contas']]
        return usuarios, contas


# Função para a criação de um novo usuário.
def criar_usuario(usuarios):

    cpfs = [x.cpf for x in usuarios]

    cpf = input('\nDigite seu CPF ou [c] para voltar ao menu principal: ')

    while True:
        if cpf == 'c':
            break
        elif not cpf.isdigit() or not len(cpf) == 11:
            cpf = input('\nCPF inválido! O CPF deve conter apenas números, 11 algarismos, incluindo os 2 dígitos finais, sem separação: ')
        elif cpf in cpfs:
            cpf = input('\nCPF já cadastrado! Digite outro CPF ou [c] para voltar ao menu principal: ')
        else:
            break
    
    if cpf == 'c':
        print('\nOperação cancelada.')
        return None
    
    nome = input('\nDigite seu nome: ')

    if nome == 'c':
        print('\nOperação cancelada.')
        return None
    
    endereco = input('\nDigite seu endereço no formato "logradouro, nro - bairro - cidade/sigla estado": ')

    while endereco.count(',') != 1 or endereco.count('-') != 2 or endereco.count('/') != 1:
        if endereco == 'c':
            break
        else:
            endereco = input('\nFormato inválido. Digite seu endereço no formato "logradouro, nro - bairro - cidade/sigla estado" ou [c] para cancelar: ')

    if endereco == 'c':
        print('\nOperação cancelada.')
        return None
    
    data_nascimento = input('\nDigite sua data de nascimento no formato DD/MM/AAAA: ')

    while True:
        if data_nascimento == 'c':
            break
        else:
            try:
                datetime.strptime(data_nascimento, "%d/%m/%Y")
                break
            except:
                data_nascimento = input('\nFormato inválido. Digite sua data de nascimento no formato DD/MM/AAAA ou [c] para cancelar: ')
        
    if data_nascimento == 'c':
        print('\nOperação cancelada.')
        return None
    
    senha = getpass.getpass('\nDigite uma senha a ser utilizada para acessar seu usuário e suas contas: ', stream=None)

    while len(senha) < 4:
        if senha == 'c':
            break
        else:
            senha = getpass.getpass('\nA senha deve conter ao menos 4 caracteres. Digite uma outra senha: ', stream=None)

    if senha == 'c':
        print('\nOperação cancelada.')
        return None

    senha_confirm = getpass.getpass('\nConfirme a senha digitada anteriormente: ', stream=None)

    while senha_confirm != senha:
        if senha_confirm == 'c':
            break
        else:
            senha_confirm = getpass.getpass('\nA segunda senha digitada é diferente da anterior. Tente novamente, ou digite [c] para cancelar: ', stream=None)

    if senha_confirm == 'c':
        print('\nOperação cancelada.')
        return None
    
    usuario = Usuario(nome, data_nascimento, cpf, endereco, senha)
    print(f'\n{repr(usuario)} criado com sucesso! Agora você pode fazer o login no menu principal.')

    return usuario


# Função para logar em um usuário.
def logar_usuario(usuarios):

    cpfs ={x.cpf: x for x in usuarios}

    cpf = input('\nDigite seu CPF ou [c] para voltar ao menu principal: ')

    while cpf not in cpfs.keys():
        if cpf == 'c':
            break
        else:
            cpf = input('\nCPF não encontrado nos usuários registrados. Lembre-se que CPFs devem conter apenas números, incluindo os dois últimos dígitos! Digite um CPF já cadastrado ou [c] para voltar ao menu principal: ')

    if cpf == 'c':
        return None
    
    usuario = cpfs[cpf]

    senha = getpass.getpass('\nDigite sua senha: ', stream=None)

    i = 1
    while senha != usuario.senha:
        if senha == 'c':
            break
        elif i < 3:
            plural = 's' if i == 1 else ''
            senha = getpass.getpass(f'\nSenha incorreta. Você tem mais {MAX_TENTATIVAS_LOGIN - i} tentativa{plural}: ', stream=None)
            i += 1
        else:
            print('\nNúmero de tentativas esgotadas. Tente novamente mais tarde.')
            break

    if senha == 'c':
        print('\nLogin cancelado, retornando ao menu principal.')
        return None
    
    if senha != usuario.senha or senha == '':
        return None
    else:
        print(f'\nLogin efetuado com sucesso em {repr(usuario)}')
        return usuario
    

# Função para criar uma conta.
def criar_conta(usuario, contas):
    apelido = input('''\nBora criar uma nova conta para você! 
A criação é muito simples, basta digitar um apelido para sua conta. Caso não queira um apelido, deixe vazio e pressione Enter.
Para cancelar a criação de uma nova conta, digite [c]: ''')

    if apelido == 'c':
        print('\nOperação cancelada!')
        return None

    if len(contas) == 0:
        novo_numero = 1
    else:
        numeros = [conta.numero for conta in contas]
        novo_numero = max(numeros) + 1

    if not apelido:
        apelido = f'{usuario.nome} {novo_numero}'

    nova_conta = Conta(usuario, AGENCIA, novo_numero, apelido)

    print(f'\nSua nova conta de apelido {apelido} foi criada com sucesso! Agora você pode acessá-la no menu de usuário.')

    return nova_conta


# Função para printar todas as contas do usuario.
def listar_contas(usuario, contas):
    contas_usuario = list(filter(lambda conta: conta.usuario.cpf == usuario.cpf, contas))

    if len(contas_usuario) == 0:
        print('\nVocê ainda não possui nenhuma conta!')

    else:
        print('\n######################################## Contas ########################################')
        for conta in contas_usuario:
            print(f'\nConta {conta.apelido}\tnúmero {conta.numero}\tSaldo: {conta.historico["saldo"]}')
        print('\n########################################################################################')


# Função para acessar uma conta.
def acessar_conta(usuario, contas):
    
    contas_usuario = list(filter(lambda conta: conta.usuario.cpf == usuario.cpf, contas))
    if len(contas_usuario) == 0:
        print('\nVocê ainda não possui nenhuma conta!')
        return None
    listar_contas(usuario, contas)

    conta_acessada = input('\nDigite o apelido ou o número da conta que você quer acessar, dentre as suas contas listadas acima: ')

    apelidos_contas_usuario = [conta.apelido for conta in contas_usuario]
    numeros_contas_usuario = [conta.numero for conta in contas_usuario]

    while conta_acessada not in apelidos_contas_usuario and int(conta_acessada) not in numeros_contas_usuario:
        if conta_acessada == 'c':
            print('\nOperação cancelada, retornando ao menu de usuário.')
            break
        else:
            conta_acessada = input('\nO apelido ou número que você digitou não existe. Tente novamente, ou digite [c] para retornar ao menu de usuário: ')

    if conta_acessada == 'c':
        return None
    
    if conta_acessada in apelidos_contas_usuario:
        contas_dict = {conta.apelido: conta for conta in contas}
        conta_acessada = contas_dict[conta_acessada]
    else:
        contas_dict = {str(conta.numero): conta for conta in contas}
        conta_acessada = contas_dict[str(conta_acessada)]
    
    return conta_acessada


# Função de depósito.
def deposito(conta_acessada, /):

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
                        conta_acessada.historico['saldo'] += valor
                        data_deposito = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        conta_acessada.historico['extrato']['data'].append(data_deposito)
                        conta_acessada.historico['extrato']['texto'].append(f'Depósito realizado no valor de R$ {valor:.2f}')
                        print(f'\nDepósito de R$ {valor:.2f} realizado com sucesso!')
                        break
                    else:
                        print('\nDepósito cancelado.')
                        break
            except:
                valor = input('\nPor favor, digite um valor numérico para seu depósito, ou [c] para cancelar a operação: ')
    
    if valor == 'c' or confirmar != 's':
        return None
    else:
        return conta_acessada


# Função de saque.
def saque(*, conta_acessada):

    # Capturando o dia de hoje
    HOJE = date.today().strftime('%Y-%m-%d')

    n_saques = conta_acessada.historico['saques'].count(HOJE)
    saldo_disponivel = conta_acessada.historico['saldo']

    if n_saques >= LIMITE_DIARIO_SAQUES:
        print(f'\nA quantidade limite de {LIMITE_DIARIO_SAQUES} saques por dia já foi atingida hoje!')
        return None
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
                    elif valor > saldo_disponivel:
                        valor = input(f'\nO valor digitado de R$ {valor:.2f} excede o saldo atual de R$ {saldo_disponivel:.2f}.\nPor favor, digite um valor válido, ou [c] para cancelar a operação: ')
                    else:
                        confirmar = input(f'\nConfirma saque no valor de R$ {valor:.2f}? [s/n]: ')

                        while confirmar not in ['s', 'n']:
                            confirmar = input('\nOpção inválida. Digite [s] para confirmar o saque ou [n] para cancelar: ')

                        if confirmar == 's':
                            conta_acessada.historico['saldo'] -= valor
                            n_saques += 1
                            data_saque = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            conta_acessada.historico['saques'].append(HOJE)
                            conta_acessada.historico['extrato']['data'].append(data_saque)
                            conta_acessada.historico['extrato']['texto'].append(f'Saque realizado no valor de R$ {valor:.2f}')
                            print(f'\nSaque de R$ {valor:.2f} realizado com sucesso!')
                            break
                        else:
                            print('\nSaque cancelado.')
                            break
                except:
                    valor = input('\nPor favor, digite um valor numérico para seu saque, ou [c] para cancelar a operação: ')

        if valor == 'c' or confirmar != 's':
            return None
        else:
            return conta_acessada


# Função de extrato.
def imprimir_extrato(saldo, /, *, extrato):
    print('\n############################## EXTRATO ##############################')
    if len(extrato['data']) == 0:
        print('Ainda não há movimentações nessa conta.')
    else:
        for data, texto in zip(extrato['data'], extrato['texto']):
            print(data, texto, sep='\t')
    print(f'\nSaldo total: {saldo:.2f}')
    print('#####################################################################\n')


# Função do menu da conta.
def menu_conta(conta_acessada):

    while True:

        MENU_CONTA = f"""
{repr(conta_acessada.usuario)} {repr(conta_acessada)}

Digite [d] para depositar;
Digite [s] para sacar;
Digite [e] para conferir o extrato e o saldo de sua conta;
Digite [q] caso deseje sair da conta e voltar ao menu de usuário.

=> """

        opcao = input(MENU_CONTA)

        if opcao == 'd':
            conta_acessada_deposito = deposito(conta_acessada)
            if conta_acessada_deposito:
                conta_acessada.historico = conta_acessada_deposito.historico

        elif opcao == 's':
            conta_acessada_saque = saque(conta_acessada=conta_acessada)
            if conta_acessada_saque:
                conta_acessada.historico = conta_acessada_saque.historico

        elif opcao == 'e':
            imprimir_extrato(conta_acessada.historico['saldo'], extrato=conta_acessada.historico['extrato'])

        elif opcao == 'q':
            sair_conta = input('\nTem certeza que deseja sair? [s/n]: ')
        
            while sair_conta not in ['s', 'n']:
                sair_conta = input('\nOpção inválida. Digite [s] caso deseje sair ou [n] para voltar ao menu da conta: ')
                
            if sair_conta == 's':
                break
        
        else:
            print('\nEntrada inválida. Confira as opções no menu da conta:')

    return conta_acessada


# Função para encerrar uma conta.
def encerrar_conta(usuario, contas):

    contas_usuario = list(filter(lambda conta: conta.usuario.cpf == usuario.cpf, contas))

    if len(contas_usuario) == 0:
        print('\nVocê não possui contas ainda!')
        return None
    
    listar_contas(usuario, contas)
    conta_encerrada = input('\nDigite o apelido ou o número da conta que você quer encerrar, dentre as suas contas listadas acima, ou [c] para cancelar a operação: ')

    apelidos_contas_usuario = [conta.apelido for conta in contas_usuario]
    numeros_contas_usuario = [conta.numero for conta in contas_usuario]

    while conta_encerrada not in apelidos_contas_usuario and int(conta_encerrada) not in numeros_contas_usuario:
        if conta_encerrada == 'c':
            print('\nOperação cancelada, retornando ao menu de usuário.')
            break
        else:
            conta_encerrada = input('\nO apelido ou número que você digitou não existe. Tente novamente, ou digite [c] para retornar ao menu de usuário: ')

    if conta_encerrada == 'c':
        return None
    
    if conta_encerrada in apelidos_contas_usuario:
        contas_dict = {conta.apelido: conta for conta in contas}
        conta_encerrada = contas_dict[conta_encerrada]
    else:
        contas_dict = {str(conta.numero): conta for conta in contas}
        conta_encerrada = contas_dict[str(conta_encerrada)]

    zerar_conta = input(f'\nPara deletar sua conta, você deve zerar antes o seu saldo. Deseja realizar a retirada de seu saldo total de R$ {conta_encerrada.historico["saldo"]:.2f}? [s/n]: ')

    while zerar_conta not in ['s', 'n']:
        zerar_conta = input('\nOpção inválida. Digite [s] caso deseje retirar todo o seu saldo e deletar sua conta ou [n] para cancelar: ')

    if zerar_conta == 's':
        print(f'\nSaldo total retirado. A conta {conta_encerrada.apelido} número {conta_encerrada.numero} foi encerrada com sucesso!')
        return conta_encerrada
    else:
        print('\nRetirada do saldo total e exclusão da conta cancelados!')
        return None


# Função para alterar a senha de usuário.
def alterar_senha(usuario):
    senha = getpass.getpass('\nDigite sua senha atual, ou [c] para cancelar: ', stream=None)

    i = 1
    while senha != usuario.senha:
        if senha == 'c':
            break
        elif i < 3:
            plural = 's' if i == 1 else ''
            senha = getpass.getpass(f'\nSenha incorreta. Você tem mais {MAX_TENTATIVAS_LOGIN - i} tentativa{plural}: ', stream=None)
            i += 1
        else:
            print('\nNúmero de tentativas esgotadas. Tente novamente mais tarde.')
            break

    if senha == 'c':
        print('\nAlteração de senha cancelada, retornando ao menu de usuário.')
        return None
    
    if senha != usuario.senha or senha == '':
        return None
    
    nova_senha = getpass.getpass('\nDigite a nova senha: ', stream=None)

    while len(nova_senha) < 4:
        if nova_senha == 'c':
            break
        else:
            nova_senha = getpass.getpass('\nA nova senha deve conter ao menos 4 caracteres. Digite uma outra senha: ', stream=None)

    if nova_senha == 'c':
        print('\nOperação cancelada.')
        return None

    senha_confirm = getpass.getpass('\nConfirme a senha digitada anteriormente: ', stream=None)

    while senha_confirm != nova_senha:
        if senha_confirm == 'c':
            break
        else:
            senha_confirm = getpass.getpass('\nA segunda senha digitada é diferente da anterior. Tente novamente, ou digite [c] para cancelar: ', stream=None)

    if senha_confirm == 'c':
        print('\nOperação cancelada.')
        return None

    return nova_senha


# Função que exclui usuario.
def excluir_usuario(usuario, contas):
    contas_usuario = list(filter(lambda conta: conta.usuario.cpf == usuario.cpf, contas))

    if len(contas_usuario) > 0:
        print('\nAntes de excluir o usuário, você precisa encessar todas as suas contas!')
        return None
    
    excluir = input(f'\n Tem certeza que deseja excluir o {usuario}? [s/n]: ')

    while excluir not in ['s', 'n']:
        excluir = input('\nOpção inválida. Digite [s] caso deseje excluir seu usuário ou [n] para cancelar: ')

    if excluir == 's':
        print(f'\nO {usuario} foi excluído com sucesso! Adeus, {usuario.nome}!')
        return excluir
    else:
        print('\nExclusão de usuário cancelada! Voltando ao menu de usuário.')
        return None


# Função do menu do usuário.
def menu_usuario(usuario, contas):

    while True:

        MENU_USUARIO = f'''
Olá, {usuario.nome}! Bem vinda(o, e) de volta!
Escolha uma das opções abaixo:

Digite [criar] para criar uma conta;
Digite [contas] para ver todas as suas contas;
Digite [acessar] para acessar uma conta;
Digite [encerrar conta] para finalizar uma conta;
Digite [logout] para deslogar e voltar ao menu principal;
Digite [nome] para alterar o nome de usuario;
Digite [senha] para alterar a senha do usuario;
Digite [excluir] para excluir o usuário.

=> '''

        opcao = input(MENU_USUARIO)

        if opcao == 'criar':
            nova_conta = criar_conta(usuario, contas)
            if nova_conta:
                contas.append(nova_conta)
            
        elif opcao == 'contas':
            listar_contas(usuario, contas)

        elif opcao == 'acessar':
            conta_acessada = acessar_conta(usuario, contas)
            if conta_acessada:
                conta_atual = menu_conta(conta_acessada)
                if conta_atual.historico != conta_acessada.historico:
                    contas.remove(conta_acessada)
                    contas.append(conta_atual)
    
        elif opcao == 'encerrar conta':
            conta_encerrada = encerrar_conta(usuario, contas)
            if conta_encerrada:
                contas.remove(conta_encerrada)

        elif opcao == 'logout':
            logout = input('\nTem certeza que deseja fazer logout e voltar ao menu principal? [s/n]: ')
        
            while logout not in ['s', 'n']:
                logout = input('\nOpção inválida. Digite [s] caso deseje sair ou [n] para voltar ao menu da conta: ')
                
            if logout == 's':
                break

        elif opcao == 'nome':
            nome = input(f'\nSeu nome atual está registrado como {usuario.nome}. Digite o novo nome que deseja para sua conta: ')
            print(f'\nNome alterado para {nome}.')
            usuario.nome = nome

        elif opcao == 'senha':
            nova_senha = alterar_senha(usuario)
            if nova_senha:
                usuario.senha = nova_senha

        elif opcao == 'excluir':
            excluir = excluir_usuario(usuario, contas)
            if excluir:
                break

        else:
            print('\nEntrada inválida. Confira as opções no menu do usuário:')

    return usuario, contas, opcao


# Função do menu principal.
def menu_principal():
    MENU_PRINCIPAL = '''
    Olá! Bem vinda(o, e) ao Banco do Fefo!
    Escolha uma das opções abaixo:

    Digite [criar] para criar um novo usuário;
    Digite [login] para fazer login em um usuário já existente;
    Digite [sair] para encerrar.
    
    => '''

    try:
        usuarios, contas = carregar_usuarios_contas()
    except:
        usuarios = []
        contas = []

    while True:
        
        opcao = input(MENU_PRINCIPAL)

        if opcao == 'criar':
            novo_usuario = criar_usuario(usuarios)
            if novo_usuario:
                usuarios.append(novo_usuario)
        
        elif opcao == 'login':
            usuario = logar_usuario(usuarios)
            if usuario:
                usuario_atual, contas, opcao = menu_usuario(usuario, contas)
                if opcao == 'excluir':
                    usuarios.remove(usuario)
                else:
                    if usuario.nome != usuario_atual.nome:
                        usuarios.remove(usuario)
                        usuarios.append(usuario_atual)

        
        elif opcao == 'sair':
            print('\nAté logo, e obrigado por utilizar o Banco do Fefo!')
            break

        else:
            print('\nOpção inválida! Retornando ao menu principal.')

    salvar_usuarios_contas(usuarios, contas)


if __name__ == "__main__":
    menu_principal()